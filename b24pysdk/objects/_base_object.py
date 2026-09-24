from abc import ABC, abstractmethod
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    FrozenSet,
    Generic,
    Iterable,
    Optional,
    Text,
    Type,
    overload,
)

from .._config import Config
from .._constants import MISSING
from ..utils.type_vars import BOPKT
from ..utils.types import JSONDict, ObjectDiscriminator, Self, Timeout, cast
from ._client_provider import ClientProvider
from ._field_accessor import FieldAccessor
from ._fields.base_field import BaseField
from ._fields.file_field import FileField
from ._filter_lookups import FilterLookup
from ._object_metadata import ObjectMetadata
from .errors import (
    BitrixObjectDoesNotExist,
    BitrixObjectFieldError,
    BitrixObjectFieldNotLoadedError,
    BitrixObjectMultipleObjectsReturned,
)

if TYPE_CHECKING:
    from ..api.requests import BitrixAPIRequest
    from ..client import ClientType

__all__ = [
    "BaseObject",
]


class BaseObject(ABC, Generic[BOPKT]):
    """Base class for SDK objects with descriptor-based Bitrix24 fields.

    The object keeps raw Bitrix24 data separately from local unsaved changes.
    Field descriptors read and write values by Bitrix24 field code only, while
    descriptors themselves are responsible for converting raw values to public
    Python values and back. Local changes can be inspected through
    ``local_data``, checked through ``has_changes``, and discarded for one
    field or for the whole object without making an API request.

    Data loaded from Bitrix24 is lazy: if ``bitrix_data`` was not passed to the
    constructor, the first read from ``bitrix_data`` or from a field descriptor
    calls ``_get_bitrix_data``. Subclasses should implement ``_get_bitrix_data``
    and ``_get_update_api_wrapper`` with concrete Bitrix24 REST methods.

    The constructor accepts either ``bitrix_pk`` for lazy loading or
    ``bitrix_data`` for an already loaded object. Fields declared with
    ``is_pk=True`` are treated as read-only SDK fields. Object metadata
    builds a converted primary-key object or raises an error if Bitrix24 data
    does not contain all primary-key fields.

    ``_FILTER_LOOKUPS`` contains explicit Django-style filter lookups supported
    by the entity REST API. Plain equality does not require a lookup and is
    always handled separately. ``_IS_COMPLETE_WITHOUT_SELECT`` describes
    whether an API response without an explicit field selection contains all
    fields registered on the object class.
    """

    OBJECT_KEY: ClassVar[Text]
    PK: Type[BOPKT]

    _IS_COMPLETE_WITHOUT_SELECT: ClassVar[bool] = True
    _UPDATE_KEY: ClassVar[Optional[Text]] = "fields"
    _USERFIELD_BITRIX_CODE_PREFIX: ClassVar[Optional[Text]] = None
    _FILTER_LOOKUPS: ClassVar[FrozenSet[FilterLookup]] = frozenset(FilterLookup.__members__.values())

    DoesNotExist: ClassVar[Type[BitrixObjectDoesNotExist]]
    MultipleObjectsReturned: ClassVar[Type[BitrixObjectMultipleObjectsReturned]]

    _meta: ClassVar[ObjectMetadata[Self]]

    _bitrix_data: Optional[JSONDict]
    _is_bitrix_data_fully_loaded: bool
    _bitrix_pk: BOPKT
    _client_provider: ClientProvider
    _local_data: Optional[JSONDict]

    def __init_subclass__(cls, *args: Any, **kwargs: Any):
        super().__init_subclass__(*args, **kwargs)
        cls._register_object_errors()
        cls._meta = ObjectMetadata(cls)

    @overload
    def __init__(
            self,
            bitrix_pk: BOPKT,
            *,
            bitrix_data: None = None,
            bitrix_data_is_complete: bool = False,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
            client_provider: Optional[ClientProvider] = None,
    ): ...

    @overload
    def __init__(
            self,
            bitrix_pk: None = None,
            *,
            bitrix_data: JSONDict,
            bitrix_data_is_complete: bool = False,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
            client_provider: Optional[ClientProvider] = None,
    ): ...

    def __init__(
            self,
            bitrix_pk: Optional[BOPKT] = None,
            *,
            bitrix_data: Optional[JSONDict] = None,
            bitrix_data_is_complete: bool = False,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
            client_provider: Optional[ClientProvider] = None,
    ):
        """Create a lazy object reference or an already loaded object.

        Exactly one of ``bitrix_pk`` and ``bitrix_data`` is required. Publicly
        supplied data is deep-copied so nested caller-owned values cannot mutate
        internal state. ``bitrix_data_is_complete`` declares whether a missing
        non-required field can be interpreted as ``None`` without reloading.
        If data is supplied, metadata extracts and converts every primary-key
        component.

        Passing an existing ``client_provider`` shares its lazily resolved
        client with objects constructed by managers and relation fields. Direct
        ``client`` and ``client_factory`` arguments create a new provider. No
        Bitrix24 request is made by the constructor.
        """

        if (bitrix_pk is None) == (bitrix_data is None):
            raise ValueError("Pass exactly one of bitrix_pk or bitrix_data.")

        if bitrix_data is None and bitrix_data_is_complete:
            raise ValueError("bitrix_data_is_complete=True requires bitrix_data.")

        if bitrix_data is not None:
            bitrix_data = self._normalize_bitrix_data(bitrix_data)

        self._bitrix_data = deepcopy(bitrix_data) if bitrix_data is not None else None
        self._is_bitrix_data_fully_loaded = bitrix_data_is_complete
        self._local_data = None

        if bitrix_pk is None:
            self._bitrix_pk = self._meta.get_bitrix_pk_from_data(self._bitrix_data)
        else:
            self._bitrix_pk = self._meta.build_bitrix_pk(bitrix_pk)

        self._client_provider = (
            ClientProvider(client=client, client_factory=client_factory)
            if client_provider is None
            else client_provider
        )

    def __repr__(self) -> Text:
        return f"<{self.__class__.__name__} bitrix_pk={self._bitrix_pk!r}>"

    def __str__(self) -> Text:
        return f"{self.__class__.__name__} {self._bitrix_pk}"

    def __eq__(self, other: "BaseObject") -> bool:
        if not isinstance(other, BaseObject) or other.__class__ is not self.__class__:
            return NotImplemented

        return self._bitrix_pk == other._bitrix_pk

    def __hash__(self) -> int:
        return hash((self.__class__, self._bitrix_pk))

    def __getitem__(self, bitrix_code: Text) -> Any:
        return self.get_field_value(bitrix_code)

    def __setitem__(self, bitrix_code: Text, value: Any):
        self.set_field_value(bitrix_code, value)

    def __delitem__(self, bitrix_code: Text):
        self.delete_field_value(bitrix_code)

    @classmethod
    def get_meta(cls) -> ObjectMetadata[Self]:
        """Return metadata registered for this SDK object class."""
        return cls._meta

    @classmethod
    def get_discriminator(cls) -> ObjectDiscriminator:
        """Return the entity discriminator used by the object registry."""
        return None

    @classmethod
    def get_required_class_params(cls) -> JSONDict:
        """Return fixed API parameters required for this object class."""
        return {}

    @classmethod
    def get_filter_lookups(cls) -> FrozenSet[FilterLookup]:
        """Return explicit filter lookups supported by the entity REST API."""
        return cls._FILTER_LOOKUPS

    @classmethod
    def supports_filter_lookup(cls, filter_lookup: FilterLookup, /) -> bool:
        """Return whether the entity REST API supports an explicit filter lookup."""
        return filter_lookup in cls.get_filter_lookups()

    @classmethod
    def _normalize_bitrix_data(cls, bitrix_data: JSONDict, /) -> JSONDict:
        """Return raw object data normalized to registered Bitrix24 field codes.

        Subclasses may override this hook when different API methods return the
        same entity with different field-name conventions. The default keeps
        the supplied mapping unchanged.
        """
        return bitrix_data

    @property
    def bitrix_pk(self) -> BOPKT:
        """Return the object primary key, if it is known."""
        return self._bitrix_pk

    @property
    def bitrix_data(self) -> JSONDict:
        """Return a detached snapshot of remote data plus local changes.

        Access lazily loads remote data if necessary. Both the stored response
        and local values are deep-copied, and local values win for matching
        Bitrix24 field codes. Mutating the returned dictionary or any nested
        value therefore cannot modify the object.
        """

        bitrix_data = deepcopy(self._get_loaded_bitrix_data())

        if self._local_data is not None:
            for bitrix_code, value in self._local_data.items():
                bitrix_data[bitrix_code] = deepcopy(value)

        return bitrix_data

    @property
    def local_data(self) -> JSONDict:
        """Return an independent copy of local unsaved changes."""
        return {} if self._local_data is None else deepcopy(self._local_data)

    @property
    def has_changes(self) -> bool:
        """Return whether this object has local unsaved field changes."""
        return self._local_data is not None

    def reset_changes(self) -> Self:
        """Discard every local unsaved change and return this object.

        Only cached projections backed by changed Bitrix24 fields are
        invalidated. Remote data is neither loaded nor modified, and no API
        request is made. Subsequent field reads therefore resolve from the
        previously loaded remote state or trigger the usual lazy load.
        """

        local_data = self._local_data

        if local_data is None:
            return self

        self._local_data = None

        for bitrix_code in local_data:
            bitrix_field = self._meta.get_field_by_bitrix_code(bitrix_code)
            self._delete_bitrix_field_cache(bitrix_field)

        return self

    def reset_field(self, name: Text):
        """Discard one local unsaved change by object attribute name.

        Args:
            name: Registered SDK field attribute name. For an ``ObjectField``,
                the local change of its source Bitrix24 field is discarded.

        Remote data is neither loaded nor modified, and no API request is made.
        If the field has no local change, this method is a no-op.
        """
        bitrix_field = self._meta.get_field(name)
        self.delete_field_value(bitrix_field.bitrix_code, bitrix_field=bitrix_field)

    def set_bitrix_data(
            self,
            bitrix_data: JSONDict,
            *,
            is_complete: bool = False,
            clear_local_data: bool = True,
            copy_data: bool = True,
    ) -> Self:
        """Replace loaded raw Bitrix24 data and return this object.

        Publicly supplied data is deep-copied by default so subsequent mutations
        of the source dictionary or its nested mutable values cannot change the
        object's internal Bitrix24 state. ``is_complete`` controls whether an
        absent non-required field means ``None`` or requires a full reload.
        Internal SDK loading paths may pass ``copy_data=False`` when ownership
        of a fresh API response is transferred directly to the object.
        """

        bitrix_data = self._normalize_bitrix_data(bitrix_data)

        self._bitrix_data = deepcopy(bitrix_data) if copy_data else bitrix_data
        self._is_bitrix_data_fully_loaded = is_complete

        if clear_local_data:
            self._local_data = None

        self._clear_bitrix_field_caches()

        return self

    @property
    def client(self) -> "ClientType":
        """Return a concrete Bitrix24 client resolved through the client provider."""
        return self._client_provider.client

    @overload
    def using(self, *, client: "ClientType", client_factory: None = None) -> Self: ...

    @overload
    def using(self, *, client: None = None, client_factory: Callable[[], "ClientType"]) -> Self: ...

    def using(
            self,
            *,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
    ) -> Self:
        """Replace the client source for this object and return itself.

        The new client source applies only to this object. It is not propagated
        to related objects that were already created and cached by object fields.
        """

        if client is None and client_factory is None:
            raise ValueError("Pass either client or client_factory.")

        if client is not None and client_factory is not None:
            raise ValueError("Pass either client or client_factory, not both.")

        self._client_provider = ClientProvider(client=client, client_factory=client_factory)

        return self

    @property
    def _base_url(self) -> Text:
        """Return the base URL of the Bitrix24 portal."""
        return f"https://{self.client.get_token().domain}"

    @abstractmethod
    def _get_bitrix_data(self) -> JSONDict:
        """Load raw object data from Bitrix24."""
        raise NotImplementedError

    @classmethod
    def _register_object_errors(cls):
        """Create per-object-class lookup exception types.

        Each concrete SDK object gets distinct ``DoesNotExist`` and
        ``MultipleObjectsReturned`` subclasses so callers can catch failures for
        one entity type specifically. An exception explicitly declared in the
        class body is preserved; merely inheriting a parent's generated type is
        not considered an override.
        """

        if "DoesNotExist" not in cls.__dict__:
            does_not_exist_error = cast(
                Type[BitrixObjectDoesNotExist],
                type(
                    "DoesNotExist",
                    (BitrixObjectDoesNotExist,),
                    {
                        "__module__": cls.__module__,
                        "__qualname__": f"{cls.__qualname__}.DoesNotExist",
                    },
                ),
            )

            cls.DoesNotExist = does_not_exist_error

        if "MultipleObjectsReturned" not in cls.__dict__:
            multiple_objects_returned_error = cast(
                Type[BitrixObjectMultipleObjectsReturned],
                type(
                    "MultipleObjectsReturned",
                    (BitrixObjectMultipleObjectsReturned,),
                    {
                        "__module__": cls.__module__,
                        "__qualname__": f"{cls.__qualname__}.MultipleObjectsReturned",
                    },
                ),
            )

            cls.MultipleObjectsReturned = multiple_objects_returned_error

    def _update(self, *, timeout: Timeout = None, **fields: Any) -> bool:
        """Update fields that remain writable after object creation."""

        if not fields:
            raise ValueError("Pass at least one field to update.")

        updated_data: JSONDict = {}

        for attr_name, value in fields.items():
            bitrix_field = self._meta.get_field(attr_name)

            bitrix_field.check_is_updatable()

            updated_data[bitrix_field.bitrix_code] = bitrix_field.to_bitrix_value(value)

        return self._send_update(updated_data, timeout=timeout)

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the update API method resolved from the supplied client."""
        raise NotImplementedError

    def _get_update_params(self, updated_data: JSONDict) -> JSONDict:
        """Build one of the update parameter shapes used by Bitrix24 APIs.

        Most endpoints expect request-name primary-key parameters plus changed
        fields under ``_UPDATE_KEY``. Endpoints that expose user fields without
        such a key expect one ``fields`` mapping containing Bitrix-code primary
        keys and changes. Remaining endpoints accept request-name primary keys
        and request-name field values directly at the top level.

        ``updated_data`` already contains raw Bitrix24 values. It is embedded by
        reference in the first shape and expanded into a new mapping in the
        other shapes; this method never mutates it.
        """

        has_update_key = self._UPDATE_KEY is not None
        has_userfields = self._USERFIELD_BITRIX_CODE_PREFIX is not None
        use_bitrix_codes = has_userfields and not has_update_key

        pk_params = dict(
            self._meta.get_bitrix_pk_items(
                self.bitrix_pk,
                use_bitrix_codes=use_bitrix_codes,
            ),
        )

        if has_update_key:
            return {
                **pk_params,
                self._UPDATE_KEY: updated_data,
                **self._meta.required_class_params,
            }

        if has_userfields:
            return {
                "fields": {
                    **pk_params,
                    **updated_data,
                },
                **self._meta.required_class_params,
            }

        fields_params = {
            self._meta.get_field_by_bitrix_code(bitrix_code).request_name: value
            for bitrix_code, value in updated_data.items()
        }

        return {
            **pk_params,
            **fields_params,
            **self._meta.required_class_params,
        }

    def _make_update_request(
            self,
            updated_data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> "BitrixAPIRequest[bool]":
        """Create a lazy update request without executing it."""
        return self._get_update_api_wrapper(self.client)(
            **self._get_update_params(updated_data),
            timeout=timeout,
        )

    def _send_update(
            self,
            updated_data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Execute an update and synchronize local state only on success.

        Empty update data is a no-op and returns ``False`` without constructing
        a request. A truthy Bitrix24 result is applied to loaded data and removes
        matching local changes. A false result leaves the object untouched so
        unsaved values remain available for inspection or retry.
        """

        if not updated_data:
            return False

        result = self._make_update_request(updated_data, timeout=timeout).result

        if result:
            self._apply_updated_data(updated_data)

        return result

    def _delete(self, *, timeout: Timeout = None) -> bool:
        """Delete this object from Bitrix24."""
        return self._make_delete_request(timeout=timeout).result

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the delete API method resolved from the supplied client."""
        raise NotImplementedError

    def _make_delete_request(self, *, timeout: Timeout = None) -> "BitrixAPIRequest[bool]":
        """Create a lazy delete request without executing it."""

        params = {
            **dict(
                self._meta.get_bitrix_pk_items(
                    self.bitrix_pk,
                    use_bitrix_codes=False,
                ),
            ),
            **self._meta.required_class_params,
        }

        return self._get_delete_api_wrapper(self.client)(**params, timeout=timeout)

    def _delete_bitrix_field_cache(self, bitrix_field: BaseField[Any, Any]):
        """Invalidate every cached projection of one source Bitrix24 field.

        A source field can feed a cached ``ObjectField`` or ``FileField``.
        Metadata indexes all such descriptors by Bitrix code so changing the raw
        value cannot leave any converted projection stale.
        """
        for cached_field in self._meta.get_cached_fields_by_bitrix_code(bitrix_field.bitrix_code):
            cached_field.delete_cached_value(self)

    def _clear_bitrix_field_caches(self):
        """Delete all cached field values."""
        for cached_field in self._meta.cached_fields:
            cached_field.delete_cached_value(self)

    def _reload_bitrix_data(self) -> JSONDict:
        """Load and return complete raw Bitrix24 data."""

        bitrix_data = self._get_bitrix_data()

        self.set_bitrix_data(
            bitrix_data,
            is_complete=True,
            clear_local_data=False,
            copy_data=False,
        )

        return bitrix_data

    def refresh(self, *, clear_local_data: bool = True) -> Self:
        """Reload object data from Bitrix24 and return this object.

        By default, local unsaved changes are discarded because fresh Bitrix24
        data becomes the new object state. Pass ``clear_local_data=False`` to
        keep local changes over the reloaded Bitrix24 data.
        """

        self.set_bitrix_data(
            self._get_bitrix_data(),
            is_complete=True,
            clear_local_data=clear_local_data,
            copy_data=False,
        )

        return self

    def _get_loaded_bitrix_data(self) -> JSONDict:
        """Return raw Bitrix24 data loaded from Bitrix24, loading it if needed."""

        bitrix_data = self._bitrix_data

        if bitrix_data is None:
            return self._reload_bitrix_data()

        return bitrix_data

    def field(self, name: Text) -> FieldAccessor:
        """Return a field accessor by object attribute name."""
        return FieldAccessor(self, self._meta.get_field(name))

    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> Dict[Text, Any]:
        """Return entity field metadata using the current client's cache.

        Field metadata is fetched through the class-level ``fields`` manager on
        the first request for an object key and discriminator pair and stored
        in the client's ``bitrix_fields`` cache. Later objects using that same
        client reuse the exact cached mapping. Different clients keep
        independent caches, which is important when portals have different
        user-field definitions.

        Raises:
            BitrixObjectFieldError: If the object class has no field manager.
        """

        object_class = self.__class__
        field_manager = getattr(object_class, "fields", None)

        if field_manager is None:
            raise BitrixObjectFieldError(
                f"{object_class.__name__} has no FieldManager. "
                "Declare a 'fields' class attribute with a BaseFieldManager instance.",
            )

        fields_cache = self.client.get_cache("bitrix_fields")
        cache_key = self.OBJECT_KEY, self.get_discriminator()
        fields = fields_cache.get(cache_key)

        if fields is None:
            fields = field_manager.using(client=self.client).list(timeout=timeout)
            fields_cache[cache_key] = fields

        return fields

    def get_field(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> Any:
        """Return cached field metadata by Bitrix24 field code."""
        try:
            return self.get_fields(timeout=timeout)[bitrix_code]
        except (KeyError, TypeError):
            raise BitrixObjectFieldError(
                f"{self.__class__.__name__} has no field metadata for {bitrix_code!r}.",
            ) from None

    def get_field_title(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> Text:
        """Return the display title of a field by Bitrix24 field code.

        Entity APIs expose field metadata in different response formats, so
        subclasses must implement extraction of a title from their concrete
        metadata source.

        Args:
            bitrix_code: Registered source Bitrix24 field code.
            timeout: Optional timeout for a metadata request made by the
                subclass implementation.

        Returns:
            The field title exposed by the concrete entity API.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support field titles.")

    def get_field_items(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> Any:
        """Return possible list values for a field by Bitrix24 field code."""
        raise NotImplementedError(f"{self.__class__.__name__} does not support list fields.")

    def get_field_value(
            self,
            bitrix_code: Text,
            *,
            bitrix_field: Optional[BaseField[Any, Any]] = None,
    ) -> Any:
        """Resolve a field value across primary-key, local, and remote state.

        Primary-key fields are a deliberate exception to the otherwise raw
        return contract: their values have already been normalized while
        constructing ``bitrix_pk``. For an object with a scalar key, the method
        returns that key directly. For an object with a composite key, it
        returns the corresponding normalized key component. Non-primary-key
        fields return their unconverted local or Bitrix24 value.

        Resolution order is deliberately strict:

        1. A normalized primary-key value or component is read from
           ``bitrix_pk`` without loading object data.
        2. A local unsaved value overrides every remote value.
        3. Remote data is loaded lazily when no data has been loaded yet.
        4. A missing field in partial data triggers one complete reload.
        5. A non-required field missing from complete data resolves to ``None``;
           a missing required field raises an SDK error.

        Args:
            bitrix_code: Source Bitrix24 field code.
            bitrix_field: Already resolved descriptor, when the caller has one.

        Returns:
            The normalized public value for a primary-key field; otherwise,
            the unconverted raw field value.

        Raises:
            BitrixObjectFieldNotLoadedError: If a required field is unavailable
                in complete Bitrix24 data.
        """

        if bitrix_field is None:
            bitrix_field = self._meta.get_field_by_bitrix_code(bitrix_code)

        # A primary key is always available independently of selected data.
        if bitrix_field.is_pk:
            if self._meta.pk_field is not None:
                return self._bitrix_pk

            return getattr(self._bitrix_pk, bitrix_field.attr_name)

        # Local writes have precedence without forcing remote data to load.
        local_data = self._local_data
        value = MISSING if local_data is None else local_data.get(bitrix_code, MISSING)

        if value is not MISSING:
            return value

        bitrix_data = self._bitrix_data

        if bitrix_data is None:
            bitrix_data = self._reload_bitrix_data()

        value = bitrix_data.get(bitrix_code, MISSING)

        if value is not MISSING:
            return value

        if not self._is_bitrix_data_fully_loaded:
            bitrix_data = self._reload_bitrix_data()
            value = bitrix_data.get(bitrix_code, MISSING)

            if value is not MISSING:
                Config().logger.warning(
                    "complete Bitrix24 object data reload returned a field "
                    "that was missing in partial data",
                    context={
                        "object_class": self.__class__.__name__,
                        "bitrix_pk": self._bitrix_pk,
                        "bitrix_code": bitrix_code,
                    },
                )

                return value

        if not bitrix_field.is_required:
            return None

        raise BitrixObjectFieldNotLoadedError(
            f"Required Bitrix field {bitrix_code!r} is registered on "
            f"{self.__class__.__name__}, but is not present in complete Bitrix data.",
        )

    def set_field_value(
            self,
            bitrix_code: Text,
            value: Any,
            *,
            bitrix_field: Optional[BaseField[Any, Any]] = None,
    ):
        """Store raw field value by Bitrix24 field code as a local change."""

        if bitrix_field is None:
            bitrix_field = self._meta.get_field_by_bitrix_code(bitrix_code)

        bitrix_field.check_is_updatable()

        if self._local_data is None:
            self._local_data = {}

        self._local_data[bitrix_code] = value
        self._delete_bitrix_field_cache(bitrix_field)

    def delete_field_value(
            self,
            bitrix_code: Text,
            *,
            bitrix_field: Optional[BaseField[Any, Any]] = None,
    ):
        """Discard a locally assigned value by Bitrix24 field code.

        The remote value is not modified. Subsequent field reads use the
        previously loaded remote value or trigger the usual lazy loading. If
        the field has no local value, this method is a no-op.
        """

        if bitrix_field is None:
            bitrix_field = self._meta.get_field_by_bitrix_code(bitrix_code)

        bitrix_field.check_is_updatable()

        local_data = self._local_data

        if local_data is None or bitrix_code not in local_data:
            return

        del local_data[bitrix_code]

        if not local_data:
            self._local_data = None

        self._delete_bitrix_field_cache(bitrix_field)

    def _apply_updated_data(self, updated_data: JSONDict):
        """Merge confirmed writes into remote state and invalidate projections.

        Matching entries are removed from local unsaved data. Ordinary raw
        values can be copied directly into loaded data, but a file write payload
        does not contain the authoritative remote file metadata; file fields are
        therefore evicted and will be reloaded on their next access. Every
        cached descriptor backed by an updated Bitrix code is invalidated.

        ``updated_data`` is only read. Ordinary values are retained by reference
        in loaded state, so internal callers and direct users of raw update APIs
        must treat the successfully applied payload as read-only afterward.
        """

        if self._bitrix_data is None:
            self._bitrix_data = {}

        local_data = self._local_data

        for bitrix_code, value in updated_data.items():
            if local_data is not None:
                local_data.pop(bitrix_code, None)

            bitrix_field = self._meta.fields_by_bitrix_code.get(bitrix_code)

            if isinstance(bitrix_field, FileField):
                self._bitrix_data.pop(bitrix_code, None)
                self._is_bitrix_data_fully_loaded = False
            else:
                self._bitrix_data[bitrix_code] = value

            if bitrix_field is not None:
                self._delete_bitrix_field_cache(bitrix_field)

        if local_data is not None and not local_data:
            self._local_data = None

    def _save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save selected raw values through the subclass update implementation.

        If ``update_fields`` is ``None``, only local unsaved changes are sent.
        ``local_data`` supplies a deep-copied snapshot, so changes made while a
        request is being handled cannot alter that request's payload.
        Otherwise, it contains SDK object attribute names, not Bitrix field codes,
        and every selected field is sent using its current raw value: a local
        unsaved value takes precedence over the loaded Bitrix24 value. Object
        fields are resolved to their source Bitrix field code.

        Fields with ``is_updatable=False``, including read-only fields, are
        rejected before any request is created. An empty local-change snapshot
        is a no-op handled by ``_send_update()``; an explicitly empty
        ``update_fields`` iterable is considered invalid.
        """

        if update_fields is None:
            updated_data = self.local_data
        else:
            updated_data = {}

            for attr_name in update_fields:
                bitrix_field = self._meta.get_field(attr_name)

                bitrix_field.check_is_updatable()

                updated_data[bitrix_field.bitrix_code] = self.get_field_value(bitrix_field.bitrix_code, bitrix_field=bitrix_field)

            if not updated_data:
                raise ValueError("Pass at least one update field or None to save all local changes.")

        return self._send_update(updated_data, timeout=timeout)
