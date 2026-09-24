from collections.abc import Set as AbstractSet
from dataclasses import asdict
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    Hashable,
    Iterable,
    List,
    Mapping,
    Optional,
    Text,
    Tuple,
    Type,
    Union,
)

from .._config import Config
from ..utils.type_vars import BOT
from ..utils.types import JSONDict, ObjectDiscriminator, cast
from ._base_pk import BasePK
from ._fields.base_cached_field import BaseCachedField
from ._fields.base_field import BaseField
from ._fields.object_field import ObjectField
from .errors import (
    BitrixObjectError,
    BitrixObjectFieldError,
    BitrixObjectFieldNotLoadedError,
)

if TYPE_CHECKING:
    from ._client_provider import ClientProvider

__all__ = [
    "ObjectMetadata",
]


class ObjectMetadata(Generic[BOT]):
    """Validated, read-only indexes for one SDK object class.

    Metadata is built when a ``BaseObject`` subclass is created. It resolves
    inherited descriptors, records primary-key order, separates concrete source
    fields from related-object projections, and precomputes cache-invalidation
    indexes. Public mappings are exposed through ``MappingProxyType`` so query
    and descriptor code can reuse them without rebuilding indexes.

    An ``ObjectField`` deliberately does not replace its source field in the
    Bitrix-code index: raw reads and writes must still use the source field's
    conversion rules. Object fields have a separate Bitrix-code index used by
    ``select_related()``. Metadata construction also registers the object class
    in ``Config`` for lazy relation resolution by object key and discriminator.
    """

    __slots__ = (
        "_bitrix_codes",
        "_cached_fields",
        "_cached_fields_by_bitrix_code",
        "_fields_by_attr_name",
        "_fields_by_bitrix_code",
        "_object_fields_by_bitrix_code",
        "_pk_bitrix_codes",
        "_pk_fields",
        "_required_class_params",
        "discriminator",
        "is_complete_without_select",
        "object_class",
        "object_key",
        "pk_type",
    )

    discriminator: ObjectDiscriminator
    is_complete_without_select: bool
    object_class: Type[BOT]
    object_key: Text
    pk_type: Type[Hashable]

    _fields_by_attr_name: Mapping[Text, BaseField[Any, Any]]
    _fields_by_bitrix_code: Mapping[Text, BaseField[Any, Any]]
    _object_fields_by_bitrix_code: Mapping[Text, ObjectField[Any]]
    _bitrix_codes: Tuple[Text, ...]
    _cached_fields: Tuple[BaseCachedField[Any, Any], ...]
    _cached_fields_by_bitrix_code: Mapping[Text, Tuple[BaseCachedField[Any, Any], ...]]
    _pk_bitrix_codes: Tuple[Text, ...]
    _pk_fields: Tuple[BaseField[Any, Any], ...]
    _required_class_params: Mapping[Text, Any]

    def __init__(self, object_class: Type[BOT], /):  # noqa: C901, PLR0912, PLR0915
        """Validate an object declaration and build all field indexes.

        Field discovery walks the MRO from base classes to the concrete class.
        A subclass descriptor replaces an inherited field with the same
        attribute name; a subclass non-field attribute removes that inherited
        field from metadata. Double underscores are rejected because they are
        reserved for filter lookup syntax.

        Concrete fields must have unique Bitrix24 codes. Every ``ObjectField``
        must reference the exact source descriptor registered as a separate
        attribute on the same object class. Object fields are indexed separately
        and may share their code with that concrete source field, but two
        different object fields may not share a code. Cached projections are
        grouped by source code so raw-value changes can invalidate all of them
        efficiently.

        Primary-key fields retain their resolved declaration order. The object
        key, primary-key type, response-completeness flag, and optional
        discriminator are validated before the class is registered globally.

        Args:
            object_class: Newly created ``BaseObject`` subclass.

        Raises:
            BitrixObjectError: If class-level identity or primary-key metadata
                is invalid.
            BitrixObjectFieldError: If field declarations conflict or use a
                reserved attribute name.
        """

        self.object_class = object_class

        # Validate class identity before scanning descriptors. A partially
        # constructed metadata object must never enter the global registry.
        try:
            object_key = getattr(object_class, "OBJECT_KEY")
        except AttributeError:
            raise BitrixObjectError(
                f"{object_class.__name__} must define the OBJECT_KEY class attribute.",
            ) from None

        if not isinstance(object_key, str) or not object_key:
            raise BitrixObjectError(
                f"{object_class.__name__}.OBJECT_KEY must be a non-empty string, "
                f"got {object_key!r}.",
            )

        try:
            pk_type = getattr(object_class, "PK")
        except AttributeError:
            raise BitrixObjectError(
                f"{object_class.__name__} must define the PK class attribute.",
            ) from None

        if not isinstance(pk_type, type):
            raise BitrixObjectError(
                f"{object_class.__name__}.PK must be a type, "
                f"got {type(pk_type).__name__!r}.",
            )

        if not issubclass(pk_type, Hashable):
            raise BitrixObjectError(
                f"{object_class.__name__}.PK must define a hashable "
                "primary-key type.",
            )

        is_complete_without_select = getattr(object_class, "_IS_COMPLETE_WITHOUT_SELECT", True)

        if not isinstance(is_complete_without_select, bool):
            raise BitrixObjectError(
                f"{object_class.__name__}._IS_COMPLETE_WITHOUT_SELECT must be bool, "
                f"got {type(is_complete_without_select).__name__!r}.",
            )

        discriminator = object_class.get_discriminator()

        self.discriminator = discriminator
        self.is_complete_without_select = is_complete_without_select
        self.object_key = object_key
        self.pk_type = pk_type
        self._required_class_params = MappingProxyType(
            dict(object_class.get_required_class_params()),
        )

        fields_by_attr_name: Dict[Text, BaseField[Any, Any]] = {}

        # Process bases first so the concrete class can replace or explicitly
        # mask inherited field descriptors.
        for base_class in reversed(cast(Tuple[Type], object_class.__mro__)):
            for attr_name, attribute in base_class.__dict__.items():
                if isinstance(attribute, BaseField):
                    if "__" in attr_name:
                        raise BitrixObjectFieldError(
                            f"Field attribute {attr_name!r} on {object_class.__name__} cannot contain '__' "
                            "because double underscores are reserved for filter lookups.",
                        )

                    fields_by_attr_name[attr_name] = attribute
                else:
                    fields_by_attr_name.pop(attr_name, None)

        fields_by_bitrix_code: Dict[Text, BaseField[Any, Any]] = {}
        object_fields_by_bitrix_code: Dict[Text, ObjectField[Any]] = {}
        cached_fields: List[BaseCachedField[Any, Any]] = []
        cached_fields_by_bitrix_code: Dict[Text, List[BaseCachedField[Any, Any]]] = {}
        pk_fields: List[BaseField[Any, Any]] = []

        concrete_field_ids: AbstractSet[int] = {
            id(field)
            for field in fields_by_attr_name.values()
            if not isinstance(field, ObjectField)
        }

        # Build lookup and cache-invalidation indexes in one pass over the final
        # descriptor set.
        for field in fields_by_attr_name.values():
            if isinstance(field, BaseCachedField):
                cached_fields.append(field)
                cached_fields_by_bitrix_code.setdefault(field.bitrix_code, []).append(field)

            if isinstance(field, ObjectField):
                # The source descriptor must remain independently addressable
                # for raw conversion, writes, and cache invalidation. Checking
                # identity is intentional: another descriptor with the same
                # Bitrix code is not the source used by this ObjectField.
                if id(field.source_field) not in concrete_field_ids:
                    raise BitrixObjectFieldError(
                        f"ObjectField {field.attr_name!r} on {object_class.__name__} "
                        f"references source field {field.source_field.bitrix_code!r}, "
                        "which is not registered as a separate field attribute "
                        "on the object class. Declare the source field first and "
                        "pass that descriptor to ObjectField().",
                    )

                existing_object_field = object_fields_by_bitrix_code.get(field.bitrix_code)

                if existing_object_field is not None and existing_object_field is not field:
                    raise BitrixObjectFieldError(
                        f"ObjectField with Bitrix code {field.bitrix_code!r} is declared more than once "
                        f"on {object_class.__name__}.",
                    )

                object_fields_by_bitrix_code[field.bitrix_code] = field
                # Keep the concrete source descriptor in
                # ``fields_by_bitrix_code`` for raw conversion and writes.
                continue

            existing_field = fields_by_bitrix_code.get(field.bitrix_code)

            if existing_field is not None and existing_field is not field:
                raise BitrixObjectFieldError(
                    f"Bitrix field {field.bitrix_code!r} is declared more than once "
                    f"on {object_class.__name__}.",
                )

            fields_by_bitrix_code[field.bitrix_code] = field

            if field.is_pk:
                pk_fields.append(field)

        # Freeze index structure after validation. Descriptor instances remain
        # shared class attributes and are not copied.
        self._fields_by_attr_name = MappingProxyType(fields_by_attr_name)
        self._fields_by_bitrix_code = MappingProxyType(fields_by_bitrix_code)
        self._object_fields_by_bitrix_code = MappingProxyType(object_fields_by_bitrix_code)
        self._bitrix_codes = tuple(fields_by_bitrix_code)
        self._cached_fields = tuple(cached_fields)
        self._cached_fields_by_bitrix_code = MappingProxyType({
            bitrix_code: tuple(fields)
            for bitrix_code, fields in cached_fields_by_bitrix_code.items()
        })
        self._pk_fields = tuple(pk_fields)
        self._pk_bitrix_codes = tuple(field.bitrix_code for field in pk_fields)

        if len(self._pk_fields) > 1 and not issubclass(self.pk_type, BasePK):
            raise BitrixObjectError(
                f"{object_class.__name__}.PK must inherit from BasePK "
                "when the object has a composite primary key.",
            )

        Config.register_object_class(
            object_key=self.object_key,
            discriminator=self.discriminator,
            object_class=object_class,
        )

    def __repr__(self) -> Text:
        return f"<{self.__class__.__name__} object_class={self.object_class.__name__!r}>"

    @property
    def fields_by_bitrix_code(self) -> Mapping[Text, BaseField[Any, Any]]:
        """Return concrete fields indexed by Bitrix24 field code."""
        return self._fields_by_bitrix_code

    @property
    def required_class_params(self) -> Mapping[Text, Any]:
        """Return fixed API parameters registered for the object class."""
        return self._required_class_params

    @property
    def bitrix_codes(self) -> Tuple[Text, ...]:
        """Return registered concrete Bitrix24 field codes in declaration order."""
        return self._bitrix_codes

    def contains_all_fields(self, bitrix_codes: Iterable[Text], /) -> bool:
        """Return whether all registered concrete fields are selected."""

        if isinstance(bitrix_codes, AbstractSet):
            selected_codes = bitrix_codes
        else:
            selected_codes = frozenset(bitrix_codes)

        return self._fields_by_bitrix_code.keys() <= selected_codes

    @property
    def cached_fields(self) -> Tuple[BaseCachedField[Any, Any], ...]:
        """Return cached fields registered on the object class."""
        return self._cached_fields

    def get_cached_fields_by_bitrix_code(self, bitrix_code: Text, /) -> Tuple[BaseCachedField[Any, Any], ...]:
        """Return cached fields associated with the supplied Bitrix24 field code."""
        return self._cached_fields_by_bitrix_code.get(bitrix_code, ())

    @property
    def pk_fields(self) -> Tuple[BaseField[Any, Any], ...]:
        """Return fields that form the object primary key."""
        return self._pk_fields

    @property
    def pk_field(self) -> Optional[BaseField[Any, Any]]:
        """Return the single primary-key field or None for a composite key."""

        if len(self._pk_fields) != 1:
            return None

        return self._pk_fields[0]

    @property
    def pk_bitrix_codes(self) -> Tuple[Text, ...]:
        """Return primary-key Bitrix24 codes in their registered order."""
        return self._pk_bitrix_codes

    def get_bitrix_pk_from_data(self, bitrix_data: JSONDict, /) -> Hashable:
        """Extract, validate, and convert a primary key from raw object data.

        Every registered primary-key field must be present. A scalar key must
        also be non-``None``. Composite-key schemas define whether individual
        components may be ``None`` and validate them in ``__post_init__``.
        Scalar values and raw composite dictionaries are normalized through
        ``build_bitrix_pk()``.

        Raises:
            BitrixObjectFieldNotLoadedError: If any primary-key field was not
                selected in the response.
            BitrixObjectFieldError: If no primary key is declared or a scalar
                primary-key value is ``None``.
        """

        if not self._pk_fields:
            raise BitrixObjectFieldError(
                f"{self.object_class.__name__} has no primary-key fields.",
            )

        bitrix_pk_data: JSONDict = {}
        is_composite_pk = len(self._pk_fields) > 1

        for bitrix_field in self._pk_fields:
            bitrix_code = bitrix_field.bitrix_code

            if bitrix_code not in bitrix_data:
                if is_composite_pk and not bitrix_field.is_required:
                    bitrix_pk_data[bitrix_code] = None
                    continue

                raise BitrixObjectFieldNotLoadedError(
                    f"Primary-key Bitrix field {bitrix_code!r} is not present "
                    f"in {self.object_class.__name__} Bitrix data.",
                )

            bitrix_pk_value = bitrix_data[bitrix_code]

            if bitrix_pk_value is None and not is_composite_pk:
                raise BitrixObjectFieldError(
                    f"Primary-key Bitrix field {bitrix_code!r} cannot be None "
                    f"for {self.object_class.__name__}.",
                )

            bitrix_pk_data[bitrix_code] = bitrix_pk_value

        return self.build_bitrix_pk(
            bitrix_pk_data
            if is_composite_pk
            else next(iter(bitrix_pk_data.values())),
        )

    def has_bitrix_pk_data(self, bitrix_data: JSONDict, /) -> bool:
        """Return whether raw Bitrix24 data contains every primary-key field."""

        is_composite_pk = len(self._pk_fields) > 1

        return bool(self._pk_fields) and all(
            bitrix_field.bitrix_code in bitrix_data
            or (is_composite_pk and not bitrix_field.is_required)
            for bitrix_field in self._pk_fields
        )

    def make_object_from_bitrix_data_or_pk(
            self,
            bitrix_data_or_pk: Union[JSONDict, Text, int],
            /,
            *,
            client_provider: "ClientProvider",
            bitrix_data_is_complete: bool = False,
    ) -> BOT:
        """Build a lazy reference or loaded object from one API result value.

        A dictionary must contain all registered primary-key codes. A partial
        dictionary containing only those codes becomes a lightweight PK-only
        object; a complete dictionary remains loaded data even when the object
        declares no other fields. Ownership of a fresh API dictionary is
        transferred to the object without a defensive copy.

        A string or integer is accepted only for an object with one primary-key
        field and creates a lazy reference. Composite keys must arrive as a data
        dictionary so each component can be extracted and converted.

        Args:
            bitrix_data_or_pk: Raw object dictionary or scalar API primary key.
            client_provider: Provider shared with the request that produced the
                value.
            bitrix_data_is_complete: Whether absent non-required fields in a
                dictionary result can be interpreted as ``None``.

        Returns:
            A new SDK object bound to the supplied client provider.

        Raises:
            TypeError: If the response shape cannot represent this object's
                primary key.
        """

        if isinstance(bitrix_data_or_pk, dict):
            bitrix_data_or_pk = self.object_class._normalize_bitrix_data(bitrix_data_or_pk)

            if not self.has_bitrix_pk_data(bitrix_data_or_pk):
                raise TypeError(
                    f"Expected {self.object_class.__name__} Bitrix data to contain "
                    "all primary-key fields.",
                )

            bitrix_pk = self.get_bitrix_pk_from_data(bitrix_data_or_pk)
            # A PK-only mapping is a relation placeholder, not proof that the
            # object's remaining fields were loaded.
            object_data = (
                None
                if not bitrix_data_is_complete and all(
                    bitrix_code in self._pk_bitrix_codes
                    for bitrix_code in bitrix_data_or_pk
                )
                else bitrix_data_or_pk
            )

            bitrix_object = self.object_class(bitrix_pk=bitrix_pk, client_provider=client_provider)

            if object_data is not None:
                bitrix_object.set_bitrix_data(
                    object_data,
                    is_complete=bitrix_data_is_complete,
                    copy_data=False,
                )

            return bitrix_object

        if isinstance(bitrix_data_or_pk, (str, int)) and not isinstance(bitrix_data_or_pk, bool):
            if len(self._pk_bitrix_codes) != 1:
                raise TypeError(
                    f"Scalar primary key cannot be used for {self.object_class.__name__} "
                    "with a composite primary key.",
                )

            return self.object_class(bitrix_pk=bitrix_data_or_pk, client_provider=client_provider)

        raise TypeError(
            "Expected Bitrix24 object data to be a dict, str, or int, "
            f"got {type(bitrix_data_or_pk).__name__}.",
        )

    def get_bitrix_pk_items(
            self,
            bitrix_pk: Any,
            *,
            use_bitrix_codes: bool,
    ) -> Tuple[Tuple[Text, Any], ...]:
        """Convert a public primary key into ordered request items.

        Scalar keys are converted through their field descriptor. Composite
        keys must be ``BasePK`` instances. Bitrix-code mode consumes
        ``to_bitrix()``; request-name mode consumes ``dataclasses.asdict()``
        and expects SDK attribute names. In both cases the key set is validated
        exactly and items are emitted in metadata primary-key order.

        Args:
            bitrix_pk: Public scalar or composite primary-key value.
            use_bitrix_codes: Use raw Bitrix24 codes instead of API-wrapper
                request names.

        Returns:
            A tuple of ordered request key/value pairs.

        Raises:
            BitrixObjectFieldError: If the object has no key, the composite-key
                protocol is invalid, or its data has missing or unknown keys.
        """

        if not self._pk_fields:
            raise BitrixObjectFieldError(
                f"{self.object_class.__name__} has no primary-key fields.",
            )

        if len(self._pk_fields) == 1:
            bitrix_field = self._pk_fields[0]
            request_key = bitrix_field.bitrix_code if use_bitrix_codes else bitrix_field.request_name

            return (
                (request_key, bitrix_field.to_bitrix_value(bitrix_pk)),
            )

        if not isinstance(bitrix_pk, BasePK):
            raise BitrixObjectFieldError(
                f"Composite primary key for {self.object_class.__name__} must be "
                "a BasePK instance.",
            )

        if use_bitrix_codes:
            bitrix_pk_data = bitrix_pk.to_bitrix()
            expected_keys = self._pk_bitrix_codes
        else:
            bitrix_pk_data = asdict(bitrix_pk)
            expected_keys = tuple(bitrix_field.attr_name for bitrix_field in self._pk_fields)

        if not isinstance(bitrix_pk_data, dict):
            raise BitrixObjectFieldError(
                f"Composite primary-key data for {self.object_class.__name__} "
                "must be a dictionary.",
            )

        actual_keys = set(bitrix_pk_data)
        expected_keys_set = set(expected_keys)
        unknown_keys = actual_keys - expected_keys_set
        missing_keys = expected_keys_set - actual_keys

        if unknown_keys:
            raise BitrixObjectFieldError(
                f"Composite primary key for {self.object_class.__name__} contains "
                f"unknown keys: {sorted(unknown_keys)!r}.",
            )

        if missing_keys:
            raise BitrixObjectFieldError(
                f"Composite primary key for {self.object_class.__name__} does not "
                f"contain keys: {sorted(missing_keys)!r}.",
            )

        return tuple(
            (key, bitrix_pk_data[key]) for key in expected_keys
        )

    def get_bitrix_codes_by_attr_name(self, attr_name: Text, /) -> Tuple[Text, ...]:
        """Return Bitrix24 codes represented by an SDK object attribute."""

        if attr_name == "bitrix_pk":
            return self._pk_bitrix_codes

        return (self.get_field(attr_name).bitrix_code,)

    def build_bitrix_pk(
            self,
            bitrix_pk_data: Union[Hashable, JSONDict],
            /,
    ) -> Hashable:
        """Normalize a public key value or raw Bitrix24 key dictionary.

        An instance of the configured key type is returned unchanged. A raw
        dictionary is accepted for a composite ``BasePK`` key and is
        deserialized through its ``from_bitrix()`` method. Scalar key types are
        constructed from a scalar value.

        Raises:
            TypeError: If a scalar is supplied for a composite key, a mapping
                is supplied for a scalar key, or the configured composite key
                does not inherit from ``BasePK``.
        """

        pk_type = self.pk_type

        if isinstance(bitrix_pk_data, pk_type):
            return bitrix_pk_data

        if isinstance(bitrix_pk_data, dict):
            if not issubclass(pk_type, BasePK):
                raise TypeError(
                    f"Raw primary-key data cannot be used for scalar "
                    f"{self.object_class.__name__}.PK.",
                )

            return pk_type.from_bitrix(bitrix_pk_data)

        if issubclass(pk_type, BasePK):
            raise TypeError(
                f"Composite primary key for {self.object_class.__name__} must "
                f"be a {pk_type.__name__} instance or raw Bitrix24 key data.",
            )

        pk_factory = cast(Callable[[Any], Hashable], pk_type)
        return pk_factory(bitrix_pk_data)

    def get_field(self, attr_name: Text) -> BaseField[Any, Any]:
        """Return a field by SDK object attribute name."""
        try:
            return self._fields_by_attr_name[attr_name]
        except KeyError:
            raise BitrixObjectFieldError(
                f"{self.object_class.__name__} has no field attribute {attr_name!r}.",
            ) from None

    def get_field_by_bitrix_code(self, bitrix_code: Text) -> BaseField[Any, Any]:
        """Return a concrete field by Bitrix24 field code."""
        try:
            return self._fields_by_bitrix_code[bitrix_code]
        except KeyError:
            raise BitrixObjectFieldError(
                f"{self.object_class.__name__} has no registered "
                f"Bitrix field {bitrix_code!r}.",
            ) from None

    def get_object_field_by_bitrix_code(self, bitrix_code: Text) -> ObjectField[Any]:
        """Return an object field by its source Bitrix24 field code."""
        try:
            return self._object_fields_by_bitrix_code[bitrix_code]
        except KeyError:
            raise BitrixObjectFieldError(
                f"{self.object_class.__name__} has no registered ObjectField "
                f"with Bitrix code {bitrix_code!r}.",
            ) from None
