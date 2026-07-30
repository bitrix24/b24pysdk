from typing import TYPE_CHECKING, Callable, Generic, Hashable, Iterable, List, Optional, Text, Union, overload

from ..schemas.api import BitrixObjectBatchWriteResponse
from ..utils.type_vars import BOT
from ..utils.types import Self, Timeout
from ._client_provider import ClientProvider
from .errors import BitrixObjectError

if TYPE_CHECKING:
    from ..client import ClientType

__all__ = [
    "BitrixObjectList",
]


class BitrixObjectList(list[BOT], Generic[BOT]):
    """Typed list of SDK objects with small object-specific helpers."""

    __slots__ = ("_client_provider",)

    _client_provider: ClientProvider

    def __init__(
            self,
            iterable: Iterable[BOT] = (),
            /,
            *,
            client_provider: Optional[ClientProvider] = None,
    ):
        if client_provider is None and isinstance(iterable, BitrixObjectList):
            client_provider = iterable._client_provider

        super().__init__(iterable)
        self._client_provider = client_provider or ClientProvider()

    def __repr__(self) -> Text:
        return f"{self.__class__.__name__}({super().__repr__()})"

    @overload
    def __getitem__(self, item: int) -> BOT: ...

    @overload
    def __getitem__(self, item: slice) -> Self: ...

    def __getitem__(self, item: Union[int, slice]) -> Union[BOT, Self]:
        value = super().__getitem__(item)

        if isinstance(item, slice):
            return self.__class__(value, client_provider=self._client_provider)

        return value

    def copy(self) -> Self:
        """Return a shallow copy preserving the object-list type."""
        return self.__class__(super().copy(), client_provider=self._client_provider)

    @property
    def _client(self) -> "ClientType":
        """Return a concrete Bitrix24 client resolved through the client provider."""
        return self._client_provider.client

    @property
    def length(self) -> int:
        """Return the number of objects in the list."""
        return len(self)

    def exists(self) -> bool:
        """Return whether the list contains at least one object."""
        return bool(self)

    def first(self) -> Optional[BOT]:
        """Return the first object, if any."""

        if self:
            return self[0]

        return None

    def last(self) -> Optional[BOT]:
        """Return the last object, if any."""

        if self:
            return self[-1]

        return None

    def to_pks(self) -> List[Hashable]:
        """Return Bitrix24 primary keys for all objects."""
        return [bitrix_object.bitrix_pk for bitrix_object in self]

    def update(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResponse:
        """Update objects using their local unsaved changes."""

        batch_requests = {}
        update_context_by_batch_key = {}

        for counter, bitrix_object in enumerate(self, start=1):
            if not hasattr(bitrix_object, "update"):
                raise BitrixObjectError(f"{type(bitrix_object).__name__} does not support update().")

            updated_data = bitrix_object._get_local_data()

            if not updated_data:
                continue

            batch_key = str(counter)

            update_context_by_batch_key[batch_key] = bitrix_object, updated_data
            batch_requests[batch_key] = bitrix_object._make_update_request(updated_data, timeout=timeout)

        if not batch_requests:
            return {
                "results": {},
                "errors": {},
            }

        batch_result = self._client.call_batches(batch_requests, timeout=timeout).result

        results = {}
        errors = {}

        for batch_key, value in (batch_result.result or {}).items():
            bitrix_object, updated_data = update_context_by_batch_key[batch_key]

            if value:
                bitrix_object._apply_updated_data(updated_data)

            results[bitrix_object.bitrix_pk] = value

        for batch_key, value in (batch_result.result_error or {}).items():
            bitrix_object, _ = update_context_by_batch_key[batch_key]
            errors[bitrix_object.bitrix_pk] = value

        return {
            "results": results,
            "errors": errors,
        }

    def delete(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResponse:
        """Delete all objects in the list and return batch results by object primary key."""

        if not self:
            return {
                "results": {},
                "errors": {},
            }

        batch_requests = {}
        bitrix_pks_by_batch_key = {}

        for counter, bitrix_object in enumerate(self, start=1):
            if not hasattr(bitrix_object, "delete"):
                raise BitrixObjectError(f"{type(bitrix_object).__name__} does not support delete().")

            batch_key = str(counter)

            bitrix_pks_by_batch_key[batch_key] = bitrix_object.bitrix_pk
            batch_requests[batch_key] = bitrix_object._make_delete_request(timeout=timeout)

        batch_result = self._client.call_batches(batch_requests, timeout=timeout).result

        results = {}
        errors = {}

        for batch_key, value in (batch_result.result or {}).items():
            results[bitrix_pks_by_batch_key[batch_key]] = value

        for batch_key, value in (batch_result.result_error or {}).items():
            errors[bitrix_pks_by_batch_key[batch_key]] = value

        return {
            "results": results,
            "errors": errors,
        }

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
        """Store an explicit client source on this list and return it."""

        if client is None and client_factory is None:
            raise ValueError("Pass either client or client_factory.")

        if client is not None and client_factory is not None:
            raise ValueError("Pass either client or client_factory, not both.")

        self._client_provider = ClientProvider(client=client, client_factory=client_factory)

        return self
