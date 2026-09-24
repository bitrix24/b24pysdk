from typing import TYPE_CHECKING, Callable, Dict, Generic, Hashable, Iterable, List, Optional, Text, Union, overload

from ..utils.type_vars import BOT
from ..utils.types import B24APIResult, JSONDict, Self, Timeout
from ._client_provider import ClientProvider
from .errors import BitrixObjectError

if TYPE_CHECKING:
    from ..api.requests import BitrixAPIRequest
    from ..client import ClientType

__all__ = [
    "BitrixObjectBatchAddResult",
    "BitrixObjectBatchWriteResult",
    "BitrixObjectList",
]


class BitrixObjectList(list[BOT], Generic[BOT]):
    """Materialized SDK objects plus a provider for list-level operations.

    Object instances keep their own client providers. The provider stored on
    this list is used only for operations that coordinate the collection, such
    as batch update and delete. Slices and ``copy()`` preserve that provider and
    create a shallow list: contained SDK objects are intentionally shared.
    """

    __slots__ = ("_client_provider",)

    _client_provider: ClientProvider

    def __init__(
            self,
            iterable: Iterable[BOT] = (),
            /,
            *,
            client_provider: Optional[ClientProvider] = None,
    ):
        """Materialize ``iterable`` and select a list-level client provider.

        Constructing from another ``BitrixObjectList`` inherits its provider
        unless one is supplied explicitly. Other iterables use a new provider,
        which can later resolve the SDK default client if needed.
        """

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
        return self.__class__(self, client_provider=self._client_provider)

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

    def update(  # noqa: C901
            self,
            updated_data: Optional[JSONDict] = None,
            /,
            *,
            timeout: Timeout = None,
    ) -> "BitrixObjectBatchWriteResult[BOT]":
        """Update eligible objects through one logical batch operation.

        ``updated_data`` is raw data keyed by Bitrix24 field codes and is reused
        for every object when supplied. The mapping is treated as read-only and
        is not copied per object. If it is ``None``, each object's ``local_data``
        property provides an independent snapshot; objects without local changes
        are skipped.

        Request objects are created first and passed together to the client,
        which may split them into protocol-sized batches. Numeric results are
        converted to booleans. For each truthy success result, exactly the data sent for that object is applied to its loaded
        state. False success values and API errors are reported without marking
        fields clean. If the list is empty, or every local snapshot is empty, no
        client call is made.

        Args:
            updated_data: Shared raw update payload, or ``None`` to use each
                object's local unsaved changes.
            timeout: Optional timeout for request construction and batch calls.

        Returns:
            Objects mapped to successful results and errors separately.

        Raises:
            ValueError: If an explicitly supplied payload is empty.
            BitrixObjectError: If any object has no public ``update()`` support.
        """

        if updated_data is not None and not updated_data:
            raise ValueError("Pass at least one field to update.")

        batch_requests: Dict[Text, "BitrixAPIRequest[bool]"] = {}
        bitrix_objects_by_batch_key: Dict[Text, BOT] = {}
        updated_data_by_batch_key: Dict[Text, JSONDict] = {}

        for counter, bitrix_object in enumerate(self, start=1):
            if not hasattr(bitrix_object, "update"):
                raise BitrixObjectError(
                    f"{type(bitrix_object).__name__} does not support update().",
                )

            object_updated_data = bitrix_object.local_data if updated_data is None else updated_data

            if not object_updated_data:
                continue

            batch_key = str(counter)

            bitrix_objects_by_batch_key[batch_key] = bitrix_object

            if updated_data is None:
                # Retain the exact snapshot used to construct this request so a
                # later local edit cannot change what is marked as persisted.
                updated_data_by_batch_key[batch_key] = object_updated_data

            batch_requests[batch_key] = bitrix_object._make_update_request(object_updated_data, timeout=timeout)

        result: Dict[BOT, B24APIResult] = {}
        result_error: Dict[BOT, B24APIResult] = {}

        if not batch_requests:
            return BitrixObjectBatchWriteResult(
                result=result,
                result_error=result_error,
                client_provider=self._client_provider,
            )

        batch_result = self._client.call_batches(batch_requests, timeout=timeout).result

        for batch_key, value in (batch_result.result or {}).items():
            bitrix_object = bitrix_objects_by_batch_key[batch_key]

            if updated_data is None:
                object_updated_data = updated_data_by_batch_key[batch_key]
            else:
                object_updated_data = updated_data

            if value:
                bitrix_object._apply_updated_data(object_updated_data)

            result[bitrix_object] = value if isinstance(value, bool) else bool(value)

        for batch_key, value in (batch_result.result_error or {}).items():
            bitrix_object = bitrix_objects_by_batch_key[batch_key]
            result_error[bitrix_object] = value

        return BitrixObjectBatchWriteResult(
            result=result,
            result_error=result_error,
            client_provider=self._client_provider,
        )

    def delete(
            self,
            *,
            timeout: Timeout = None,
    ) -> "BitrixObjectBatchWriteResult[BOT]":
        """Delete all objects through one logical batch operation.

        Each object contributes one lazy delete request. The list-level client
        executes the request collection and results are translated from internal
        string batch keys back to object instances. An empty list short-circuits
        without resolving a client or making an API call.

        Raises:
            BitrixObjectError: If any contained object has no public
                ``delete()`` support.
        """

        result: Dict[BOT, B24APIResult] = {}
        result_error: Dict[BOT, B24APIResult] = {}

        if not self:
            return BitrixObjectBatchWriteResult(
                result=result,
                result_error=result_error,
                client_provider=self._client_provider,
            )

        batch_requests = {}
        bitrix_objects_by_batch_key = {}

        for counter, bitrix_object in enumerate(self, start=1):
            if not hasattr(bitrix_object, "delete"):
                raise BitrixObjectError(f"{type(bitrix_object).__name__} does not support delete().")

            batch_key = str(counter)

            bitrix_objects_by_batch_key[batch_key] = bitrix_object
            batch_requests[batch_key] = bitrix_object._make_delete_request(timeout=timeout)

        batch_result = self._client.call_batches(batch_requests, timeout=timeout).result

        for batch_key, value in (batch_result.result or {}).items():
            result[bitrix_objects_by_batch_key[batch_key]] = value

        for batch_key, value in (batch_result.result_error or {}).items():
            result_error[bitrix_objects_by_batch_key[batch_key]] = value

        return BitrixObjectBatchWriteResult(
            result=result,
            result_error=result_error,
            client_provider=self._client_provider,
        )

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
        """Store an explicit client source on this list and return it.

        The new client source applies only to list-level operations. It is not
        propagated to objects already contained in the list, so their own client
        providers remain unchanged.
        """

        if client is None and client_factory is None:
            raise ValueError("Pass either client or client_factory.")

        if client is not None and client_factory is not None:
            raise ValueError("Pass either client or client_factory, not both.")

        self._client_provider = ClientProvider(client=client, client_factory=client_factory)

        return self


class BitrixObjectBatchAddResult(Generic[BOT]):
    """Successful objects and caller-keyed errors from a bulk add operation."""

    __slots__ = ("errors", "results")

    errors: Dict[Hashable, B24APIResult]
    results: BitrixObjectList[BOT]

    def __init__(
            self,
            *,
            results: BitrixObjectList[BOT],
            errors: Dict[Hashable, B24APIResult],
    ):
        self.results = results
        self.errors = errors

    @property
    def is_success(self) -> bool:
        """Return whether the batch add completed without errors."""
        return not self.has_errors

    @property
    def has_errors(self) -> bool:
        """Return whether the batch add contains any errors."""
        return bool(self.errors)


class BitrixObjectBatchWriteResult(Generic[BOT]):
    """Object-keyed success and error mappings from a bulk write operation.

    ``results`` and ``errors`` expose fresh ``BitrixObjectList`` views over the
    mapping keys and preserve the provider used for the originating list-level
    operation. The raw API values remain available in ``result`` and
    ``result_error``.
    """

    __slots__ = ("_client_provider", "result", "result_error")

    _client_provider: ClientProvider
    result: Dict[BOT, B24APIResult]
    result_error: Dict[BOT, B24APIResult]

    def __init__(
            self,
            *,
            result: Dict[BOT, B24APIResult],
            result_error: Dict[BOT, B24APIResult],
            client_provider: Optional[ClientProvider] = None,
    ):
        self._client_provider = client_provider or ClientProvider()
        self.result = result
        self.result_error = result_error

    @property
    def is_success(self) -> bool:
        """Return whether the batch write completed without errors."""
        return not self.has_errors

    @property
    def has_errors(self) -> bool:
        """Return whether the batch write contains any errors."""
        return bool(self.result_error)

    @property
    def results(self) -> BitrixObjectList[BOT]:
        """Return objects whose bulk write operation succeeded."""
        return BitrixObjectList(self.result, client_provider=self._client_provider)

    @property
    def errors(self) -> BitrixObjectList[BOT]:
        """Return objects whose bulk write operation failed."""
        return BitrixObjectList(self.result_error, client_provider=self._client_provider)
