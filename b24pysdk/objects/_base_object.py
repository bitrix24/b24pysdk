from abc import ABC, abstractmethod
from dataclasses import asdict, is_dataclass
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Generic, Iterable, Optional, Text, Tuple, Type, overload

from .._config import Config
from ..utils.type_vars import BOPKT, BOT
from ..utils.types import JSONDict, Timeout, cast
from ._client_provider import ClientProvider
from ._field_accessor import FieldAccessor
from ._object_metadata import ObjectMetadata
from .errors import (
    BitrixObjectDoesNotExist,
    BitrixObjectFieldError,
    BitrixObjectFieldNotLoadedError,
    BitrixObjectFieldReadOnlyError,
    BitrixObjectMultipleObjectsReturned,
)
from .fields.base_field import BaseField

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
    Python values and back.

    Data loaded from Bitrix24 is lazy: if ``bitrix_data`` was not passed to the
    constructor, the first read from ``bitrix_data`` or from a field descriptor
    calls ``_get_bitrix_data``. Subclasses should implement ``_get_bitrix_data``
    and ``_get_update_api_wrapper`` with concrete Bitrix24 REST methods.

    The constructor accepts either ``bitrix_pk`` for lazy loading or
    ``bitrix_data`` for an already loaded object. Fields declared with
    ``is_pk=True`` are treated as read-only SDK fields. ``_get_bitrix_pk_from_data``
    returns a converted primary-key object or raises an error if Bitrix24 data
    does not contain all primary-key fields.
    """

    _PK_TYPE: Type[BOPKT]
    _UPDATE_KEY: ClassVar[Optional[Text]] = "fields"
    _USERFIELD_AVAILABLE: ClassVar[bool] = False

    DoesNotExist: ClassVar[Type[BitrixObjectDoesNotExist]]
    MultipleObjectsReturned: ClassVar[Type[BitrixObjectMultipleObjectsReturned]]

    _meta: ClassVar[ObjectMetadata]

    _bitrix_data: Optional[JSONDict]
    _bitrix_pk: BOPKT
    _client_provider: ClientProvider
    _local_data: JSONDict

    def __init_subclass__(cls, *args: Any, **kwargs: Any):
        super().__init_subclass__(*args, **kwargs)
        cls._register_object_errors()
        cls._meta = ObjectMetadata(cls)

    @overload
    def __init__(
            self,
            bitrix_pk: BOPKT,
            *,
            bitrix_data: Optional[JSONDict] = None,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
    ): ...

    @overload
    def __init__(
            self,
            bitrix_pk: Optional[BOPKT] = None,
            *,
            bitrix_data: JSONDict,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
    ): ...

    def __init__(
            self,
            bitrix_pk: Optional[BOPKT] = None,
            *,
            bitrix_data: Optional[JSONDict] = None,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
    ):
        if bitrix_pk is None and bitrix_data is None:
            raise ValueError("Pass either bitrix_pk or bitrix_data.")

        self._bitrix_data = dict(bitrix_data) if bitrix_data is not None else None
        self._client_provider = ClientProvider(client=client, client_factory=client_factory)
        self._local_data = {}

        if bitrix_pk is None:
            self._bitrix_pk = self._get_bitrix_pk_from_data(self._bitrix_data)
        else:
            self._bitrix_pk = self._meta.build_bitrix_pk(bitrix_pk)

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

    @property
    def bitrix_pk(self) -> BOPKT:
        """Return the object primary key, if it is known."""
        return self._bitrix_pk

    @property
    def bitrix_data(self) -> JSONDict:
        """Return Bitrix24 data merged with local unsaved changes."""

        bitrix_data = dict(self._get_loaded_bitrix_data())
        bitrix_data.update(self._local_data)

        return bitrix_data

    @property
    def client(self) -> "ClientType":
        """Return a concrete Bitrix24 client resolved through the client provider."""
        return self._client_provider.client

    @property
    def _base_url(self) -> Text:
        """Return the base URL of the Bitrix24 portal."""
        return f"https://{self.client.get_token().domain}"

    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> Any:
        """Return all field metadata cached by the current client."""

        object_class = self.__class__
        field_manager = getattr(object_class, "fields", None)

        if field_manager is None:
            raise BitrixObjectFieldError(
                f"{object_class.__name__} has no FieldManager. "
                "Declare a 'fields' class attribute with a BaseFieldManager instance.",
            )

        fields_cache = self.client.get_cache("fields")

        try:
            return fields_cache[object_class]
        except KeyError:
            fields = field_manager.using(client=self.client).list(timeout=timeout)
            self.client.set_cache("fields", {object_class: fields})
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

    @overload
    def using(self: BOT, *, client: "ClientType", client_factory: None = None) -> BOT: ...

    @overload
    def using(self: BOT, *, client: None = None, client_factory: Callable[[], "ClientType"]) -> BOT: ...

    def using(
            self: BOT,
            *,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
    ) -> BOT:
        """Replace the client source for this object and return itself."""

        if client is None and client_factory is None:
            raise ValueError("Pass either client or client_factory.")

        if client is not None and client_factory is not None:
            raise ValueError("Pass either client or client_factory, not both.")

        self._client_provider = ClientProvider(client=client, client_factory=client_factory)

        return self

    @abstractmethod
    def _get_bitrix_data(self) -> JSONDict:
        """Load raw object data from Bitrix24."""
        raise NotImplementedError

    def _update(self, *, timeout: Timeout = None, **fields: Any) -> bool:
        """Update object fields from SDK attribute names and Python values."""

        if not fields:
            raise ValueError("Pass at least one field to update.")

        updated_data: JSONDict = {}

        for attr_name, value in fields.items():
            bitrix_field = self._meta.get_field(attr_name)

            if bitrix_field.is_read_only:
                raise BitrixObjectFieldReadOnlyError(f"Field {bitrix_field.attr_name!r} is read-only.")

            updated_data[bitrix_field.bitrix_code] = bitrix_field.to_bitrix_value(value)

        return self._send_update(updated_data, timeout=timeout)

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the update API method resolved from the supplied client."""
        raise NotImplementedError

    def _get_update_params(self, updated_data: JSONDict) -> JSONDict:
        """Build update method parameters from primary key and updated data."""

        has_update_key = self._UPDATE_KEY is not None
        use_bitrix_codes = self._USERFIELD_AVAILABLE and not has_update_key

        pk_params = dict(
            self._get_bitrix_pk_items(
                self.bitrix_pk,
                has_key=use_bitrix_codes,
            ),
        )

        if has_update_key:
            return {
                **pk_params,
                self._UPDATE_KEY: updated_data,
            }

        if self._USERFIELD_AVAILABLE:
            return {
                "fields": {
                    **pk_params,
                    **updated_data,
                },
            }

        fields_params = {
            self._meta.get_field_by_bitrix_code(bitrix_code).request_name: value
            for bitrix_code, value in updated_data.items()
        }

        return {
            **pk_params,
            **fields_params,
        }

    def _get_local_data(self) -> JSONDict:
        """Return a copy of local unsaved changes."""
        return dict(self._local_data)

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
        """Send an update request and synchronize the object data."""

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
        return self._get_delete_api_wrapper(self.client)(self.bitrix_pk, timeout=timeout)

    def field(self, name: Text) -> FieldAccessor:
        """Return a field accessor by object attribute name."""
        return FieldAccessor(self, self._meta.get_field(name))

    @classmethod
    def _get_bitrix_pk_from_data(cls, bitrix_data: JSONDict) -> BOPKT:
        """Return a primary-key object built from Bitrix24 data."""

        if not cls._meta.pk_fields:
            raise BitrixObjectFieldError(f"{cls.__name__} has no primary-key fields.")

        bitrix_pk_values = []

        for bitrix_field in cls._meta.pk_fields:
            bitrix_code = bitrix_field.bitrix_code

            if bitrix_code not in bitrix_data:
                raise BitrixObjectFieldNotLoadedError(
                    f"Primary-key Bitrix field {bitrix_code!r} is not present "
                    f"in {cls.__name__} Bitrix data.",
                )

            bitrix_pk_values.append(bitrix_data[bitrix_code])

        return cls._meta.build_bitrix_pk(*bitrix_pk_values)

    @classmethod
    def _get_bitrix_pk_items(cls, bitrix_pk: Any, has_key: bool) -> Iterable[Tuple[Text, Any]]:
        """Yield filter items for a primary-key value."""

        pk_fields = cls._meta.pk_fields

        if not pk_fields:
            raise BitrixObjectFieldError(f"{cls.__name__} has no primary-key fields.")

        if len(pk_fields) == 1:
            bitrix_field = pk_fields[0]
            filter_key = bitrix_field.bitrix_code if has_key else bitrix_field.request_name
            yield filter_key, bitrix_field.to_bitrix_value(bitrix_pk)
            return

        to_bitrix = getattr(bitrix_pk, "to_bitrix", None)

        if not (is_dataclass(bitrix_pk) and callable(to_bitrix)):
            raise BitrixObjectFieldError(
                f"Composite primary key filter for {cls.__name__} must be a BaseSchema dataclass "
                f"with a to_bitrix() method.",
            )

        if not has_key:
            bitrix_pk_data = asdict(bitrix_pk)
            expected_filter_keys = {bitrix_field.attr_name for bitrix_field in pk_fields}
        else:
            bitrix_pk_data = to_bitrix()
            expected_filter_keys = {bitrix_field.bitrix_code for bitrix_field in pk_fields}

        if not isinstance(bitrix_pk_data, dict):
            raise BitrixObjectFieldError(
                f"Composite primary key filter data for {cls.__name__} must be a dictionary.",
            )

        filter_keys = set(bitrix_pk_data)
        unknown_filter_keys = filter_keys - expected_filter_keys
        missing_filter_keys = expected_filter_keys - filter_keys

        if unknown_filter_keys:
            raise BitrixObjectFieldError(
                f"Composite primary key filter for {cls.__name__} contains unknown keys: "
                f"{sorted(unknown_filter_keys)!r}.",
            )

        if missing_filter_keys:
            raise BitrixObjectFieldError(
                f"Composite primary key filter for {cls.__name__} does not contain keys: "
                f"{sorted(missing_filter_keys)!r}.",
            )

        for filter_key, bitrix_value in bitrix_pk_data.items():
            yield filter_key, bitrix_value

    @classmethod
    def _register_object_errors(cls):
        """Create object-specific lookup errors for this SDK object class."""

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

    def _delete_bitrix_field_private_attr(self, bitrix_field: BaseField[Any, Any]):
        """Delete a private field cache for one registered Bitrix field."""
        bitrix_field.delete_private_attr(self)

    def _clear_bitrix_field_private_attrs(self):
        """Delete private field caches for all registered Bitrix fields."""
        for bitrix_field in self._meta.fields_by_bitrix_code.values():
            self._delete_bitrix_field_private_attr(bitrix_field)

    def _update_bitrix_data(
            self,
            bitrix_data: JSONDict,
            *,
            clear_local_data: bool = False,
    ):
        """Replace loaded raw Bitrix24 data."""

        self._bitrix_data = dict(bitrix_data)

        if clear_local_data:
            self._local_data.clear()

        self._clear_bitrix_field_private_attrs()

    def _reload_bitrix_data(self):
        """Load fresh raw Bitrix24 data and store it separately from local data."""
        self._update_bitrix_data(self._get_bitrix_data())

    def refresh(self: BOT, *, clear_local_data: bool = True) -> BOT:
        """Reload object data from Bitrix24 and return this object.

        By default, local unsaved changes are discarded because fresh Bitrix24
        data becomes the new object state. Pass ``clear_local_data=False`` to
        keep local changes over the reloaded Bitrix24 data.
        """

        self._update_bitrix_data(
            self._get_bitrix_data(),
            clear_local_data=clear_local_data,
        )

        return self

    def _get_loaded_bitrix_data(self) -> JSONDict:
        """Return raw Bitrix24 data loaded from Bitrix24, loading it if needed."""

        if self._bitrix_data is None:
            self._reload_bitrix_data()

        return self._bitrix_data

    def get_field_value(self, bitrix_code: Text) -> Any:
        """Return a raw field value by Bitrix24 field code."""

        bitrix_field = self._meta.get_field_by_bitrix_code(bitrix_code)

        if bitrix_field.is_pk:
            if self._meta.pk_field is not None:
                return self._bitrix_pk

            return getattr(self._bitrix_pk, bitrix_field.attr_name)

        try:
            return self._local_data[bitrix_code]
        except KeyError:
            pass

        bitrix_data = self._bitrix_data
        was_loaded = bitrix_data is not None

        if not was_loaded:
            self._reload_bitrix_data()
            bitrix_data = self._bitrix_data

        try:
            return bitrix_data[bitrix_code]
        except KeyError:
            if bitrix_field.is_missing_allowed:
                return None

            if not was_loaded:
                raise BitrixObjectFieldNotLoadedError(
                    f"Bitrix field {bitrix_code!r} is registered on "
                    f"{self.__class__.__name__}, but is not present in Bitrix data.",
                ) from None

        self._reload_bitrix_data()
        bitrix_data = self._bitrix_data

        try:
            value = bitrix_data[bitrix_code]
        except KeyError:
            raise BitrixObjectFieldNotLoadedError(
                f"Bitrix field {bitrix_code!r} is registered on "
                f"{self.__class__.__name__}, but is not present in Bitrix data.",
            ) from None

        Config().logger.warning(
            "extra Bitrix24 object data reload returned a field "
            "that was missing in already loaded data",
            context={
                "object_class": self.__class__.__name__,
                "bitrix_pk": self._bitrix_pk,
                "bitrix_code": bitrix_code,
            },
        )

        return value

    def set_field_value(self, bitrix_code: Text, value: Any):
        """Store raw field value by Bitrix24 field code as a local change."""

        bitrix_field = self._meta.get_field_by_bitrix_code(bitrix_code)

        if bitrix_field.is_read_only:
            raise BitrixObjectFieldReadOnlyError(f"Field {bitrix_field.attr_name!r} is read-only.")

        self._local_data[bitrix_code] = value
        self._delete_bitrix_field_private_attr(bitrix_field)

    def delete_field_value(self, bitrix_code: Text):
        """Remove a local unsaved field value by Bitrix24 field code."""

        bitrix_field = self._meta.get_field_by_bitrix_code(bitrix_code)

        if bitrix_field.is_read_only:
            raise BitrixObjectFieldReadOnlyError(f"Field {bitrix_field.attr_name!r} is read-only.")

        if bitrix_code in self._local_data:
            del self._local_data[bitrix_code]
            self._delete_bitrix_field_private_attr(bitrix_field)

    def _apply_updated_data(self, updated_data: JSONDict):
        """Merge successfully updated values into Bitrix24 data and mark them clean."""

        if self._bitrix_data is None:
            self._bitrix_data = {}

        self._bitrix_data.update(updated_data)

        for bitrix_code in updated_data:
            self._local_data.pop(bitrix_code, None)

            bitrix_field = self._meta.fields_by_bitrix_code.get(bitrix_code)

            if bitrix_field is not None:
                self._delete_bitrix_field_private_attr(bitrix_field)

    def _save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save local changes through the subclass ``_update`` implementation.

        ``update_fields`` contains SDK object attribute names, not Bitrix field
        codes. Object fields are resolved to their source Bitrix field code.
        """

        if update_fields is None:
            local_data = dict(self._local_data)
        else:
            update_fields = tuple(update_fields)

            if not update_fields:
                raise ValueError(
                    "Pass at least one update field or None to save all local changes.",
                )

            update_bitrix_codes = (
                self._meta.get_field(attr_name).bitrix_code
                for attr_name in update_fields
            )

            local_data = {
                bitrix_code: self._local_data[bitrix_code]
                for bitrix_code in update_bitrix_codes
                if bitrix_code in self._local_data
            }

        return self._send_update(local_data, timeout=timeout)
