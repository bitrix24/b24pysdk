from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Generator, Generic, Iterable, Iterator, List, Optional, Text, Tuple, Type, Union

from ....schemas.api import BitrixObjectBatchWriteResponse
from ....utils.type_vars import BOT
from ....utils.types import DefaultTimeout, JSONDict, Self, Timeout, cast
from ..._bitrix_object_list import BitrixObjectList
from ..._client_provider import ClientProvider
from ...errors import BitrixObjectError, BitrixObjectFieldError
from .._base_manager import BaseManager
from ._object_query_state import ObjectQueryState

if TYPE_CHECKING:
    from ....api.requests import BitrixAPIValueRequest, BitrixAPIValuesListFastRequest, BitrixAPIValuesListRequest, BitrixAPIValuesRequest
    from ....client import ClientType

__all__ = [
    "BaseObjectManager",
]


class BaseObjectManager(BaseManager[BOT], ABC, Generic[BOT]):
    """Base descriptor and query builder for SDK object managers.

    The manager is intended to be declared on an SDK object class::

        class Deal(BaseObject[int]):
            objects = DealManager()

    Access through the object class returns a manager bound to that object
    class. Access through an object instance is not allowed.

    Protected query builder methods (``_filter``, ``_order`` and ``_select``)
    return manager copies and are intended to be exposed by concrete managers
    with public names. Query methods make a manager iterable lazily, while
    ``first`` and ``last`` execute the current query and return one object or
    ``None``. Fast queries may expose one-pass values iterators.
    """

    _FILTER_KEY: ClassVar[Optional[Text]] = "filter"
    _ORDER_KEY: ClassVar[Optional[Text]] = "order"
    _SELECT_KEY: ClassVar[Text] = "select"
    _ADD_KEY: ClassVar[Optional[Text]] = "fields"

    __slots__ = (
        "_api_wrapper",
        "_query_state",
        "_response",
    )

    _api_wrapper: Optional[Callable[["ClientType"], Callable[..., "BitrixAPIValuesRequest[Any, BOT]"]]]
    _query_state: ObjectQueryState
    _response: Optional[Union[BitrixObjectList[BOT], Generator[BOT, None, None]]]

    def __init__(
            self,
            *,
            object_class: Optional[Type[BOT]] = None,
            client_provider: Optional[ClientProvider] = None,
            api_wrapper: Optional[Callable[["ClientType"], Callable[..., "BitrixAPIValuesRequest[Any, BOT]"]]] = None,
            query_state: Optional[ObjectQueryState] = None,
    ):
        super().__init__(
            object_class=object_class,
            client_provider=client_provider,
        )

        self._api_wrapper = api_wrapper
        self._query_state = ObjectQueryState() if query_state is None else query_state
        self._response = None

    def __iter__(self) -> Iterator[BOT]:
        """Iterate over objects for the current query.

        Fast mode may return a one-pass iterator.
        """
        return iter(self._get_response())

    def __contains__(self, bitrix_object: BOT) -> bool:
        """Return whether the current result query contains an object."""
        return bitrix_object in self.to_list()

    @property
    def _filter_param(self) -> Optional[JSONDict]:
        """Return a copy of the current filtering parameters."""
        filter_param = self._query_state.filter_param
        return dict(filter_param) if filter_param is not None else None

    @property
    def _order_param(self) -> Optional[JSONDict]:
        """Return a copy of the current ordering parameters."""
        order_param = self._query_state.order_param
        return dict(order_param) if order_param is not None else None

    @property
    def _select_param(self) -> Optional[List[Text]]:
        """Return a copy of the selected Bitrix24 field codes."""
        select_param = self._query_state.select_param
        return list(select_param) if select_param is not None else None

    @property
    def _kwargs(self) -> Optional[JSONDict]:
        """Return a copy of additional request parameters."""
        kwargs = self._query_state.kwargs
        return dict(kwargs) if kwargs is not None else None

    @property
    def _limit_param(self) -> Optional[int]:
        """Return the current result limit."""
        return self._query_state.limit_param

    @property
    def _start_param(self) -> Optional[int]:
        """Return the current pagination offset."""
        return self._query_state.start_param

    @property
    def _timeout(self) -> Timeout:
        """Return the current request timeout."""
        return self._query_state.timeout

    @property
    def _is_fast(self) -> bool:
        """Return whether fast list loading is enabled."""
        return self._query_state.is_fast

    @property
    def _is_reversed(self) -> bool:
        """Return whether result ordering is reversed."""
        return self._query_state.is_reversed

    @property
    def _is_result_query(self) -> bool:
        """Return whether this manager represents an executable query."""
        return self._query_state.is_result_query

    def _get_response(self) -> Union[BitrixObjectList[BOT], Generator[BOT, None, None]]:
        """Return cached objects or load them lazily for the current query."""

        if not self._is_result_query:
            raise TypeError("Object manager has no result query. Call a query method before accessing results.")

        if self._response is None:
            self._response = cast(
                Union[BitrixObjectList[BOT], Generator[BOT, None, None]],
                self._make_list_request().response.values,
            )

        return self._response

    def timeout(self, timeout: DefaultTimeout) -> Self:
        """Return a manager copy with a request timeout."""

        if timeout is None:
            raise ValueError("Timeout cannot be None.")

        return self._clone(
            query_state=self._query_state.with_timeout(timeout),
        )

    def all(self) -> Self:
        """Return a lazy iterable manager for the current query."""
        return self._clone(
            query_state=self._query_state.with_is_result_query(True),
        )

    def as_fast(self, is_fast: bool = True) -> Self:
        """Return a lazy iterable manager with fast one-pass loading enabled or disabled."""

        if is_fast and self._start_param is not None:
            raise BitrixObjectError("Fast list loading does not support start offset.")

        return self._clone(
            query_state=self._query_state.with_is_fast(is_fast),
        )

    def to_list(self) -> BitrixObjectList[BOT]:
        """Execute the current query and return results as a typed object list."""

        response = self._get_response()

        if isinstance(response, BitrixObjectList):
            return response

        bitrix_object_list = BitrixObjectList(response, client_provider=self._client_provider)
        self._response = bitrix_object_list

        return bitrix_object_list

    def _add(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BOT:
        """Create a Bitrix24 object from SDK field values and return it."""
        return self._make_add_request(
            self._get_add_params(fields),
            timeout=timeout,
        ).response.value

    def _add_many(
            self,
            items: Iterable[JSONDict],
            *,
            ignore_errors: bool = False,
            timeout: Timeout = None,
    ) -> BitrixObjectList[BOT]:
        """
        Create many Bitrix24 objects from SDK field dictionaries.

        By default, the method treats any creation error as a failure of the
        whole operation. When ``ignore_errors`` is ``True``, failed items are
        skipped and the method returns only successfully created objects.
        """

        batch_requests = {}

        for counter, fields in enumerate(items, start=1):
            batch_requests[counter] = self._make_add_request(
                self._get_add_params(fields),
                timeout=timeout,
            )

        if not batch_requests:
            return BitrixObjectList(client_provider=self._client_provider)

        batch_result = self._client.call_batches(
            batch_requests,
            halt=not ignore_errors,
            timeout=timeout,
        ).result

        if batch_result.result_error and not ignore_errors:
            raise BitrixObjectError(
                f"BitrixObjectManager._add_many() got batch errors: {batch_result.result_error!r}.",
            )

        bitrix_objects = BitrixObjectList(client_provider=self._client_provider)

        for bitrix_result in (batch_result.result or {}).values():
            bitrix_objects.append(self._make_object_from_add_result(bitrix_result))

        return bitrix_objects

    def _make_object_from_add_result(self, bitrix_result: Union[JSONDict, Text, int], /) -> BOT:
        """Build an SDK object from an optionally wrapped add result."""

        object_meta = self._meta

        if isinstance(bitrix_result, dict) and not object_meta.has_bitrix_pk_data(bitrix_result):
            if len(bitrix_result) != 1:
                raise BitrixObjectError(
                    f"Cannot build {object_meta.object_class.__name__}: expected all "
                    "primary-key Bitrix fields or exactly one wrapper key.",
                )

            bitrix_result = next(iter(bitrix_result.values()))

        try:
            return object_meta.make_object_from_bitrix_data_or_pk(bitrix_result, client=self._client)
        except (TypeError, ValueError, BitrixObjectFieldError) as error:
            raise BitrixObjectError(
                f"Cannot build {object_meta.object_class.__name__} from "
                f"Bitrix24 add result: {error}",
            ) from error

    def _get_objects_for_write(self) -> BitrixObjectList[BOT]:
        """Load objects for update or delete, selecting only primary keys when supported."""

        if hasattr(self, "select"):
            return self._clone(
                query_state=self._query_state.with_select_param(self._meta.pk_bitrix_codes),
            ).to_list()

        return self.to_list()

    def _update(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BitrixObjectBatchWriteResponse:
        """Load matching objects, apply field changes and update them in batches."""

        if not fields:
            raise ValueError("Pass at least one field to update.")

        bitrix_objects = self._get_objects_for_write()

        for bitrix_object in bitrix_objects:
            for attr_name, value in fields.items():
                setattr(bitrix_object, attr_name, value)

        return bitrix_objects.update(timeout=timeout)

    def _delete(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResponse:
        """Load matching objects and delete them in batches."""
        return self._get_objects_for_write().delete(timeout=timeout)

    def count(self) -> int:
        """Return the number of loaded objects in the current result query."""
        return self.to_list().length

    def exists(self) -> bool:
        """Return whether the current result query contains at least one object."""
        return self.to_list().exists()

    def first(self) -> Optional[BOT]:
        """Execute the current query with limit ``1`` and return the first object, if any."""

        for bitrix_object in self.limit(1):
            return bitrix_object

        return None

    def last(self) -> Optional[BOT]:
        """Execute the reversed current query with limit ``1`` and return the first object, if any."""
        return self.reverse().first()

    def limit(self, limit: Optional[int]) -> Self:
        """Return a lazy iterable manager with a maximum number of objects.

        Pass ``None`` to clear an existing limit.
        """

        if limit is not None and (not isinstance(limit, int) or isinstance(limit, bool) or limit < 1):
            raise ValueError("Limit must be a positive integer or None.")

        return self._clone(
            query_state=self._query_state.with_limit_param(limit),
        )

    def reverse(self) -> Self:
        """Return a lazy iterable manager with reversed ordering."""
        return self._clone(
            query_state=self._query_state.with_is_reversed(not self._is_reversed),
        )

    def _start(self, start: Optional[int]) -> Self:
        """Return a lazy iterable manager with a custom Bitrix24 ``start`` offset.

        Pass ``None`` to clear an existing start offset.
        """

        if start is not None and (not isinstance(start, int) or isinstance(start, bool) or start < 0):
            raise ValueError("Start must be a non-negative integer or None.")

        if start is not None and self._is_fast:
            raise BitrixObjectError("Fast list loading does not support start offset.")

        return self._clone(
            query_state=self._query_state.with_start_param(start),
        )

    def _filter(self, filter_params: Optional[JSONDict] = None, /, **filters: Any) -> Self:
        """Return a manager copy with additional raw and SDK field filters."""

        if not (filter_params or filters):
            raise ValueError("Pass at least one filter.")

        filter_param = self._filter_param or {}

        if filter_params:
            filter_param.update(filter_params)

        for attr_name, value in filters.items():
            for filter_key, bitrix_value in self._get_filter_items(attr_name, value):
                filter_param[filter_key] = bitrix_value

        return self._clone(
            query_state=self._query_state.with_filter_param(filter_param),
        )

    def _get_filter_items(
            self,
            attr_name: Text,
            value: Any,
    ) -> Iterable[Tuple[Text, Any]]:
        """Return Bitrix24 filter items for an SDK object attribute."""

        use_bitrix_codes = self._FILTER_KEY is not None

        if attr_name == "bitrix_pk":
            return self._meta.get_bitrix_pk_items(
                value,
                use_bitrix_codes=use_bitrix_codes,
            )

        bitrix_field = self._meta.get_field(attr_name)
        filter_key = bitrix_field.bitrix_code if use_bitrix_codes else bitrix_field.request_name

        return (
            (filter_key, bitrix_field.to_bitrix_value(value)),
        )

    def _order(self, *fields: Text) -> Self:
        """Return a manager copy with additional ordering parameters."""

        if not fields:
            raise ValueError("Pass at least one order field.")

        order_param = self._order_param or {}

        for field_name in fields:
            direction = "ASC"
            clean_field_name = field_name

            if clean_field_name.startswith("-"):
                direction = "DESC"
                clean_field_name = clean_field_name[1:]

            if not clean_field_name:
                raise BitrixObjectFieldError("Order field name cannot be empty.")

            for bitrix_code in self._meta.get_bitrix_codes_by_attr_name(clean_field_name):
                order_param.pop(bitrix_code, None)
                order_param[bitrix_code] = direction

        return self._clone(
            query_state=self._query_state.with_order_param(order_param),
        )

    def _select(self, *fields: Text) -> Self:
        """Return a manager copy with additional select parameters."""

        if not fields:
            raise ValueError("Pass at least one select field.")

        select_param = self._select_param or []

        for attr_name in fields:
            if not attr_name:
                raise BitrixObjectFieldError("Select field name cannot be empty.")

            for bitrix_code in self._meta.get_bitrix_codes_by_attr_name(attr_name):
                if bitrix_code not in select_param:
                    select_param.append(bitrix_code)

        return self._clone(
            query_state=self._query_state.with_select_param(select_param),
        )

    def _with_api_wrapper(self, api_wrapper: Callable[["ClientType"], Callable[..., "BitrixAPIValuesRequest[Any, BOT]"]]) -> Self:
        """Return a manager copy using another API wrapper."""
        return self._clone(api_wrapper=api_wrapper)

    def _with_params(self, **kwargs: Any) -> Self:
        """Return a manager copy with additional top-level request parameters."""

        if not kwargs:
            raise ValueError("Pass at least one request parameter.")

        request_kwargs = self._kwargs
        request_kwargs = request_kwargs if request_kwargs is not None else {}
        request_kwargs.update(kwargs)

        return self._clone(
            query_state=self._query_state.with_kwargs(request_kwargs),
        )

    def _get_add_params(self, fields: JSONDict) -> JSONDict:
        """Return Bitrix24 add method parameters from SDK object field values."""

        if not fields:
            raise ValueError("Pass at least one field to add.")

        add_fields: JSONDict = {}

        for attr_name, value in fields.items():
            bitrix_field = self._meta.get_field(attr_name)

            if bitrix_field.is_read_only:
                raise BitrixObjectFieldError(f"Field {bitrix_field.attr_name!r} is read-only.")

            field_key = bitrix_field.request_name if self._ADD_KEY is None else bitrix_field.bitrix_code
            add_fields[field_key] = bitrix_field.to_bitrix_value(value)

        if self._ADD_KEY is None:
            return add_fields

        return {self._ADD_KEY: add_fields}

    @abstractmethod
    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[Any, BOT]"]:
        """Return the load API method resolved from the supplied client."""
        raise NotImplementedError

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[Any, BOT]"]:
        """Return the add API method resolved from the supplied client."""
        raise NotImplementedError

    def _make_add_request(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> "BitrixAPIValueRequest[Any, BOT]":
        """Create a lazy value request for the concrete Bitrix24 add method."""
        return self._get_add_api_wrapper(self._client)(**params, timeout=timeout)

    def _clone(
            self,
            *,
            object_class: Optional[Type[BOT]] = None,
            client_provider: Optional[ClientProvider] = None,
            api_wrapper: Optional[Callable[["ClientType"], Callable[..., "BitrixAPIValuesRequest[Any, BOT]"]]] = None,
            query_state: Optional[ObjectQueryState] = None,
    ) -> Self:
        """Return a manager copy with updated binding or query state."""
        return self.__class__(
            object_class=self._object_class if object_class is None else object_class,
            client_provider=self._client_provider if client_provider is None else client_provider,
            api_wrapper=self._api_wrapper if api_wrapper is None else api_wrapper,
            query_state=self._query_state if query_state is None else query_state,
        )

    def _get_order_param(self) -> Optional[JSONDict]:
        """Return ordering parameters with ``reverse()`` applied."""

        if not self._is_reversed:
            return self._order_param

        if not self._order_param:
            return dict.fromkeys(self._meta.pk_bitrix_codes, "DESC")

        return {
            bitrix_code: "ASC" if direction == "DESC" else "DESC"
            for bitrix_code, direction in self._order_param.items()
        }

    @property
    def _fast_descending(self) -> bool:
        """Return whether fast list loading should traverse primary keys in descending order."""

        order_param = self._get_order_param()

        if not order_param:
            return False

        pk_bitrix_codes = set(self._meta.pk_bitrix_codes)

        if set(order_param) != pk_bitrix_codes:
            raise BitrixObjectError("Fast list loading supports ordering only by primary key.")

        directions = set(order_param.values())

        if directions == {"DESC"}:
            return True

        if directions == {"ASC"}:
            return False

        raise BitrixObjectError("Fast list loading does not support mixed primary-key ordering.")

    def _get_params(self) -> JSONDict:
        """Return Bitrix24 list method parameters for the current query state."""

        params = dict(self._kwargs) if self._kwargs is not None else {}

        self._add_filter_param(params)
        self._add_order_param(params)
        self._add_select_param(params)
        self._add_start_param(params)

        return params

    def _add_filter_param(self, params: JSONDict):
        """Add filtering parameters to top-level Bitrix24 request parameters."""

        if self._filter_param is None:
            return

        if self._FILTER_KEY is None:
            params.update(self._filter_param)
        else:
            params[self._FILTER_KEY] = dict(self._filter_param)

    def _add_order_param(self, params: JSONDict):
        """Add ordering parameters to top-level Bitrix24 request parameters."""

        if self._is_fast:
            return

        order_param = self._get_order_param()

        if order_param is None:
            return

        if self._ORDER_KEY is None:
            params.update(order_param)
        else:
            params[self._ORDER_KEY] = dict(order_param)

    def _add_select_param(self, params: JSONDict):
        """Add select parameters to top-level Bitrix24 request parameters."""

        if self._select_param is None:
            return

        select_param = list(self._select_param)

        for bitrix_code in self._meta.pk_bitrix_codes:
            if bitrix_code not in select_param:
                select_param.append(bitrix_code)

        params[self._SELECT_KEY] = select_param

    def _add_start_param(self, params: JSONDict):
        """Add Bitrix24 pagination start offset to top-level request parameters."""

        if self._start_param is not None:
            if self._is_fast:
                raise BitrixObjectError("Fast list loading does not support start offset.")

            params["start"] = self._start_param

    def _make_request(self, params: JSONDict) -> "BitrixAPIValuesRequest[Any, BOT]":
        """Create a lazy values request for the current query."""

        api_wrapper_resolver = self._get_api_wrapper if self._api_wrapper is None else self._api_wrapper
        api_wrapper = api_wrapper_resolver(self._client)

        return api_wrapper(**params, timeout=self._timeout)

    def _make_list_request(self) -> Union["BitrixAPIValuesListRequest[BOT]", "BitrixAPIValuesListFastRequest[BOT]"]:
        """Create a lazy values-list request for the current query."""

        request = self._make_request(self._get_params())

        if self._is_fast:
            return request.as_list_fast(
                descending=self._fast_descending,
                limit=self._limit_param,
            )
        else:
            return request.as_list(limit=self._limit_param)
