from dataclasses import asdict, is_dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Hashable, Iterable, List, Mapping, Optional, Text, Tuple, Type, Union

from .._config import Config
from ..utils.type_vars import BOT
from ..utils.types import JSONDict, cast
from ._fields.base_field import BaseField
from ._fields.object_field import ObjectField
from .errors import BitrixObjectError, BitrixObjectFieldError, BitrixObjectFieldNotLoadedError

if TYPE_CHECKING:
    from ..client import ClientType

__all__ = [
    "ObjectMetadata",
]


class ObjectMetadata(Generic[BOT]):
    """Immutable field metadata for an SDK object class."""

    __slots__ = (
        "_fields_by_attr_name",
        "_fields_by_bitrix_code",
        "_object_fields_by_source_field",
        "_pk_bitrix_codes",
        "_pk_fields",
        "discriminator",
        "object_class",
        "object_key",
        "pk_type",
    )

    discriminator: Optional[int]
    object_class: Type[BOT]
    object_key: Text
    pk_type: Type[Hashable]

    _fields_by_attr_name: Mapping[Text, BaseField[Any, Any]]
    _fields_by_bitrix_code: Mapping[Text, BaseField[Any, Any]]
    _object_fields_by_source_field: Mapping[BaseField[Any, Any], Tuple[ObjectField[Any], ...]]
    _pk_bitrix_codes: Tuple[Text, ...]
    _pk_fields: Tuple[BaseField[Any, Any], ...]

    def __init__(self, object_class: Type[BOT], /):  # noqa: C901, PLR0912, PLR0915
        self.object_class = object_class

        try:
            object_key = getattr(object_class, "_OBJECT_KEY")
        except AttributeError:
            raise BitrixObjectError(
                f"{object_class.__name__} must define the _OBJECT_KEY class attribute.",
            ) from None

        if not isinstance(object_key, str) or not object_key:
            raise BitrixObjectError(
                f"{object_class.__name__}._OBJECT_KEY must be a non-empty string, "
                f"got {object_key!r}.",
            )

        try:
            pk_type = getattr(object_class, "_PK_TYPE")
        except AttributeError:
            raise BitrixObjectError(
                f"{object_class.__name__} must define the _PK_TYPE class attribute.",
            ) from None

        if not isinstance(pk_type, type):
            raise BitrixObjectError(
                f"{object_class.__name__}._PK_TYPE must be a type, "
                f"got {type(pk_type).__name__!r}.",
            )

        if not issubclass(pk_type, Hashable):
            raise BitrixObjectError(
                f"{object_class.__name__}._PK_TYPE must define a hashable "
                "primary-key type.",
            )

        discriminator = object_class.get_discriminator()

        if discriminator is not None and (not isinstance(discriminator, int) or isinstance(discriminator, bool)):
            raise BitrixObjectError(
                f"{object_class.__name__}.get_discriminator() must return int or None, "
                f"got {type(discriminator).__name__!r}.",
            )

        self.discriminator = discriminator
        self.object_key = object_key
        self.pk_type = pk_type

        fields_by_attr_name: Dict[Text, BaseField[Any, Any]] = {}

        for base_class in reversed(cast(Tuple[Type], object_class.__mro__)):
            for attr_name, attribute in base_class.__dict__.items():
                if isinstance(attribute, BaseField):
                    fields_by_attr_name[attr_name] = attribute
                else:
                    fields_by_attr_name.pop(attr_name, None)

        fields_by_bitrix_code: Dict[Text, BaseField[Any, Any]] = {}
        object_fields_by_attr_name: Dict[Text, ObjectField[Any]] = {}
        pk_fields: List[BaseField[Any, Any]] = []

        for attr_name, field in fields_by_attr_name.items():
            if isinstance(field, ObjectField):
                object_fields_by_attr_name[attr_name] = field
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

        object_fields_by_source_field: Dict[BaseField[Any, Any], List[ObjectField[Any]]] = {}

        for attr_name, object_field in object_fields_by_attr_name.items():
            source_field = object_field.source_field
            registered_source_field = fields_by_bitrix_code.get(source_field.bitrix_code)

            if registered_source_field is None:
                raise BitrixObjectFieldError(
                    f"Object field {attr_name!r} uses unregistered source field "
                    f"{source_field.bitrix_code!r} on {object_class.__name__}.",
                )

            if registered_source_field is not source_field:
                raise BitrixObjectFieldError(
                    f"Object field {attr_name!r} uses source field "
                    f"{source_field.bitrix_code!r} that was overridden "
                    f"on {object_class.__name__}.",
                )

            object_fields_by_source_field.setdefault(source_field, []).append(object_field)

        self._fields_by_attr_name = MappingProxyType(fields_by_attr_name)
        self._fields_by_bitrix_code = MappingProxyType(fields_by_bitrix_code)
        self._object_fields_by_source_field = MappingProxyType({
            source_field: tuple(object_fields)
            for source_field, object_fields in object_fields_by_source_field.items()
        })
        self._pk_fields = tuple(pk_fields)
        self._pk_bitrix_codes = tuple(field.bitrix_code for field in pk_fields)

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

    def get_object_fields_by_source_field(self, source_field: BaseField[Any, Any], /) -> Tuple[ObjectField[Any], ...]:
        """Return object fields whose related primary key is stored in the source field."""
        return self._object_fields_by_source_field.get(source_field, ())

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
        """Build the object primary key from raw Bitrix24 data."""

        if not self._pk_fields:
            raise BitrixObjectFieldError(
                f"{self.object_class.__name__} has no primary-key fields.",
            )

        bitrix_pk_values = []

        for bitrix_field in self._pk_fields:
            bitrix_code = bitrix_field.bitrix_code

            if bitrix_code not in bitrix_data:
                raise BitrixObjectFieldNotLoadedError(
                    f"Primary-key Bitrix field {bitrix_code!r} is not present "
                    f"in {self.object_class.__name__} Bitrix data.",
                )

            bitrix_pk_value = bitrix_data[bitrix_code]

            if bitrix_pk_value is None:
                raise BitrixObjectFieldError(
                    f"Primary-key Bitrix field {bitrix_code!r} cannot be None "
                    f"for {self.object_class.__name__}.",
                )

            bitrix_pk_values.append(bitrix_pk_value)

        return self.build_bitrix_pk(*bitrix_pk_values)

    def has_bitrix_pk_data(self, bitrix_data: Mapping[Text, Any], /) -> bool:
        """Return whether raw Bitrix24 data contains every primary-key field."""
        return bool(self._pk_bitrix_codes) and all(
            bitrix_code in bitrix_data
            for bitrix_code in self._pk_bitrix_codes
        )

    def make_object_from_bitrix_data_or_pk(
            self,
            bitrix_data_or_pk: Union[JSONDict, Text, int],
            /,
            *,
            client: "ClientType",
    ) -> BOT:
        """Build an SDK object from full Bitrix24 data or primary-key data."""

        if isinstance(bitrix_data_or_pk, dict):
            if not self.has_bitrix_pk_data(bitrix_data_or_pk):
                raise TypeError(
                    f"Expected {self.object_class.__name__} Bitrix data to contain "
                    "all primary-key fields.",
                )

            bitrix_pk = self.get_bitrix_pk_from_data(bitrix_data_or_pk)
            object_data = None if len(bitrix_data_or_pk) == len(self._pk_bitrix_codes) else bitrix_data_or_pk

            return self.object_class(
                bitrix_pk=bitrix_pk,
                bitrix_data=object_data,
                client=client,
            )

        if isinstance(bitrix_data_or_pk, (str, int)) and not isinstance(bitrix_data_or_pk, bool):
            if len(self._pk_bitrix_codes) != 1:
                raise TypeError(
                    f"Scalar primary key cannot be used for {self.object_class.__name__} "
                    "with a composite primary key.",
                )

            return self.object_class(bitrix_pk=bitrix_data_or_pk, client=client)

        raise TypeError(
            "Expected Bitrix24 object data to be a dict, str, or int, "
            f"got {type(bitrix_data_or_pk).__name__}.",
        )

    def get_bitrix_pk_items(
            self,
            bitrix_pk: Any,
            *,
            use_bitrix_codes: bool,
    ) -> Iterable[Tuple[Text, Any]]:
        """Return request items for an object primary-key value."""

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

        to_bitrix = getattr(bitrix_pk, "to_bitrix", None)

        if not (is_dataclass(bitrix_pk) and callable(to_bitrix)):
            raise BitrixObjectFieldError(
                f"Composite primary key for {self.object_class.__name__} must be "
                "a BaseSchema dataclass with a to_bitrix() method.",
            )

        if use_bitrix_codes:
            bitrix_pk_data = to_bitrix()
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

        return (
            (key, bitrix_pk_data[key]) for key in expected_keys
        )

    def get_bitrix_codes_by_attr_name(self, attr_name: Text, /) -> Iterable[Text]:
        """Return Bitrix24 codes represented by an SDK object attribute."""

        if attr_name == "bitrix_pk":
            return self._pk_bitrix_codes

        return (self.get_field(attr_name).bitrix_code,)

    def build_bitrix_pk(self, *values: Any) -> Hashable:
        """Build the public primary-key value from raw Bitrix24 values."""

        if not values:
            raise ValueError("Pass at least one primary-key value.")

        if len(values) == 1 and isinstance(values[0], self.pk_type):
            return values[0]

        pk_factory = cast(Callable[..., Hashable], self.pk_type)
        return pk_factory(*values)

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
