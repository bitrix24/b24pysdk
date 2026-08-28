from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, Generator, Generic, Hashable, Iterable, Iterator, List, Mapping, Optional, Sequence, Text, Tuple, Type, Union

from ...._config import Config
from ....utils.type_vars import BOT
from ....utils.types import B24APIResult, DefaultTimeout, JSONDict, Self, Timeout, cast
from ..._client_provider import ClientProvider
from ..._fields.object_field import ObjectField
from ..._filter_lookups import FilterLookup
from ..._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult, BitrixObjectList
from ...errors import BitrixObjectError, BitrixObjectFieldError, BitrixObjectFieldReadOnlyError, BitrixObjectFilterError
from .._base_manager import BaseManager
from ._object_query_state import ObjectQueryState

if TYPE_CHECKING:
    from ....api.requests import BitrixAPIValueRequest, BitrixAPIValuesListFastRequest, BitrixAPIValuesListRequest, BitrixAPIValuesRequest
    from ....client import ClientType
    from ..._base_object import BaseObject

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

        if self._response is None:
            self._response = cast(
                Union[BitrixObjectList[BOT], Generator[BOT, None, None]],
                self._make_list_request().values,
            )

            if self._query_state.select_related_param is not None:
                if not isinstance(self._response, BitrixObjectList):
                    self._response = BitrixObjectList(self._response, client_provider=self._client_provider)

                self._load_select_related(self._response)

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
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[BOT]:
        """Create many Bitrix24 objects and return successful objects and errors."""

        batch_requests: Dict[Text, "BitrixAPIValueRequest[Any, BOT]"] = {}
        item_keys_by_batch_key: Dict[Text, Hashable] = {}

        if isinstance(objects_data, Mapping):
            objects_items = objects_data.items()
        else:
            objects_items = enumerate(objects_data)

        for counter, (item_key, object_data) in enumerate(objects_items, start=1):
            batch_key = str(counter)
            item_keys_by_batch_key[batch_key] = item_key
            batch_requests[batch_key] = self._make_add_request(
                self._get_add_params(object_data),
                timeout=timeout,
            )

        bitrix_objects = BitrixObjectList(client_provider=self._client_provider)
        errors: Dict[Hashable, B24APIResult] = {}

        if not batch_requests:
            return BitrixObjectBatchAddResult(
                results=bitrix_objects,
                errors=errors,
            )

        batch_result = self._client.call_batches(batch_requests, timeout=timeout).result

        for bitrix_result in (batch_result.result or {}).values():
            bitrix_objects.append(self._make_object_from_add_result(bitrix_result))

        for batch_key, error in (batch_result.result_error or {}).items():
            errors[item_keys_by_batch_key[batch_key]] = error

        return BitrixObjectBatchAddResult(
            results=bitrix_objects,
            errors=errors,
        )

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
            return object_meta.make_object_from_bitrix_data_or_pk(bitrix_result, client_provider=self._client_provider)
        except (TypeError, ValueError, BitrixObjectFieldError) as error:
            raise BitrixObjectError(
                f"Cannot build {object_meta.object_class.__name__} from "
                f"Bitrix24 add result: {error}",
            ) from error

    def _get_objects_for_write(self) -> BitrixObjectList[BOT]:
        """Load objects for update or delete, selecting only primary keys when supported."""

        if hasattr(self, "select"):
            return self._clone(
                query_state=self._query_state.with_select_param(self._meta.pk_bitrix_codes, None),
            ).to_list()

        return self.to_list()

    def _update(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BitrixObjectBatchWriteResult[BOT]:
        """Load matching objects and update them in batches."""

        if not fields:
            raise ValueError("Pass at least one field to update.")

        updated_data: JSONDict = {}

        for attr_name, value in fields.items():
            bitrix_field = self._meta.get_field(attr_name)

            if bitrix_field.is_read_only:
                raise BitrixObjectFieldReadOnlyError(f"Field {bitrix_field.attr_name!r} is read-only.")

            updated_data[bitrix_field.bitrix_code] = bitrix_field.to_bitrix_value(value)

        return self._get_objects_for_write().update(updated_data, timeout=timeout)

    def _delete(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResult[BOT]:
        """Load matching objects and delete them in batches."""
        return self._get_objects_for_write().delete(timeout=timeout)

    def count(self) -> int:
        """Return the total number of objects matching the current filters."""

        query_state = self._query_state

        if self._start_param is not None:
            Config().logger.warning(
                "count() ignores start and returns the total number of objects matching the current filters",
                context={
                    "object_class": self._meta.object_class.__name__,
                    "start": self._start_param,
                },
            )
            query_state = query_state.with_start_param(None)

        request = self._clone(query_state=query_state)._make_request()
        total = request.response.total

        return len(request.values) if total is None else total

    def exists(self) -> bool:
        """Return whether the current result query contains at least one object."""
        return self.first() is not None

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

    def _filter(
            self,
            filter_params: Optional[JSONDict] = None,
            /,
            **filters: Any,
    ) -> Self:
        """Return a manager copy with raw filters and ``field__lookup`` SDK filters."""

        if not (filter_params or filters):
            raise ValueError("Pass at least one filter.")

        current_filter_param = self._query_state.filter_param
        filter_param = {} if current_filter_param is None else dict(current_filter_param)

        if filter_params:
            filter_param.update(filter_params)

        for attr_name, value in filters.items():
            for filter_key, bitrix_value in self._get_filter_items(attr_name, value):
                filter_param[filter_key] = bitrix_value

        return self._clone(
            query_state=self._query_state.with_filter_param(filter_param),
        )

    @staticmethod
    def _parse_filter_name(filter_name: Text, /) -> Tuple[Text, Optional[FilterLookup]]:
        """Split an SDK filter name into an attribute name and optional lookup."""

        attr_name, separator, lookup_name = filter_name.rpartition("__")

        if not separator:
            return filter_name, None

        if not attr_name or not lookup_name:
            raise BitrixObjectFilterError(f"Invalid filter name {filter_name!r}.")

        try:
            filter_lookup = FilterLookup(lookup_name)
        except ValueError:
            raise BitrixObjectFilterError(f"Unknown filter lookup {lookup_name!r}.") from None

        return attr_name, filter_lookup

    def _get_filter_items(
            self,
            filter_name: Text,
            value: Any,
    ) -> Iterable[Tuple[Text, Any]]:
        """Return Bitrix24 filter items for an SDK object attribute and lookup."""

        attr_name, filter_lookup = self._parse_filter_name(filter_name)
        use_bitrix_codes = self._FILTER_KEY is not None

        if attr_name == "bitrix_pk":
            if filter_lookup is None:
                return self._meta.get_bitrix_pk_items(
                    value,
                    use_bitrix_codes=use_bitrix_codes,
                )

            bitrix_field = self._meta.pk_field

            if bitrix_field is None:
                raise BitrixObjectFilterError(
                    "Filter lookups for 'bitrix_pk' are supported only for "
                    "objects with a single primary-key field.",
                )
        else:
            bitrix_field = self._meta.get_field(attr_name)

        filter_key = bitrix_field.bitrix_code if use_bitrix_codes else bitrix_field.request_name

        if filter_lookup is None:
            return (
                (filter_key, bitrix_field.to_bitrix_value(value)),
            )

        if self._FILTER_KEY is None:
            raise BitrixObjectFilterError(
                "Explicit filter lookups are supported only by list methods "
                "with a dedicated filter parameter.",
            )

        object_class = self._meta.object_class

        if not object_class.supports_filter_lookup(filter_lookup):
            raise BitrixObjectFilterError(
                f"{object_class.__name__} does not support filter lookup {filter_lookup.value!r}.",
            )

        filter_operator = bitrix_field.get_filter_operator(filter_lookup)

        return (
            (
                f"{filter_operator.bitrix_prefix}{filter_key}",
                filter_operator.prepare_value(bitrix_field, value),
            ),
        )

    def _order(self, *fields: Text) -> Self:
        """Return a manager copy with additional ordering parameters."""

        if not fields:
            raise ValueError("Pass at least one order field.")

        current_order_param = self._query_state.order_param
        order_param = {} if current_order_param is None else dict(current_order_param)

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

        select_param = list(self._query_state.select_param or ())
        selected_bitrix_codes = set(select_param)
        select_field_param = {
            attr_name: list(nested_fields)
            for attr_name, nested_fields in (self._query_state.select_field_param or {}).items()
        }
        object_class = self._get_object_class()

        for field_path in fields:
            if not field_path:
                raise BitrixObjectFieldError("Select field name cannot be empty.")

            attr_name, separator, nested_path = field_path.partition(".")

            if not attr_name or (separator and not nested_path):
                raise BitrixObjectFieldError(f"Invalid select field path {field_path!r}.")

            object_meta = object_class.get_meta()
            bitrix_field = object_meta.get_field(attr_name)

            if nested_path and not isinstance(bitrix_field, ObjectField):
                raise BitrixObjectFieldError(
                    f"Field {attr_name!r} on {object_class.__name__} is not an ObjectField.",
                )

            for bitrix_code in object_meta.get_bitrix_codes_by_attr_name(attr_name):
                if bitrix_code not in selected_bitrix_codes:
                    selected_bitrix_codes.add(bitrix_code)
                    select_param.append(bitrix_code)

            if nested_path:
                self._validate_select_field_path(bitrix_field.object_class, nested_path, field_path)
                nested_fields = select_field_param.setdefault(attr_name, [])

                if nested_path not in nested_fields:
                    nested_fields.append(nested_path)

        return self._clone(
            query_state=self._query_state.with_select_param(
                select_param,
                select_field_param or None,
            ),
        )

    def _from_pks(self, bitrix_pks: Iterable[Hashable]) -> Self:
        """Return objects filtered by Bitrix24 primary keys."""

        if isinstance(bitrix_pks, (str, bytes, bytearray)):
            raise TypeError("Primary keys must be passed as a non-string iterable.")

        return self._filter(bitrix_pk__in=bitrix_pks)

    def select_related(self, *fields: Text) -> Self:
        """Return a manager copy that preloads related ``ObjectField`` values."""

        if not fields:
            raise ValueError("Pass at least one related field.")

        if self._is_fast:
            raise BitrixObjectError("Fast list loading does not support select_related().")

        select_related_param = {
            attr_name: list(nested_paths)
            for attr_name, nested_paths in (self._query_state.select_related_param or {}).items()
        }

        for field_path in fields:
            self._validate_select_related_path(field_path)
            attr_name, _, nested_path = field_path.partition(".")
            nested_paths = select_related_param.setdefault(attr_name, [])

            if nested_path and nested_path not in nested_paths:
                nested_paths.append(nested_path)

        return self._clone(
            query_state=self._query_state.with_select_related_param(select_related_param),
        )

    def _validate_select_related_path(self, field_path: Text):
        """Validate one dotted related-field path."""

        if not field_path:
            raise BitrixObjectFieldError("Related field name cannot be empty.")

        object_class = self._get_object_class()

        for attr_name in field_path.split("."):
            if not attr_name:
                raise BitrixObjectFieldError(f"Invalid related field path {field_path!r}.")

            bitrix_field = object_class.get_meta().get_field(attr_name)

            if not isinstance(bitrix_field, ObjectField):
                raise BitrixObjectFieldError(
                    f"Field {attr_name!r} on {object_class.__name__} is not an ObjectField.",
                )

            object_class = bitrix_field.object_class

    def _validate_select_field_path(
            self,
            object_class: "Type[BaseObject[Any]]",
            field_path: Text,
            original_field_path: Text,
    ):
        """Validate nested select path without adding its fields to root select."""

        attr_name, _, nested_path = field_path.partition(".")

        if not attr_name:
            raise BitrixObjectFieldError(f"Invalid select field path {original_field_path!r}.")

        bitrix_field = object_class.get_meta().get_field(attr_name)

        if not nested_path:
            return

        if not isinstance(bitrix_field, ObjectField):
            raise BitrixObjectFieldError(
                f"Field {attr_name!r} on {object_class.__name__} is not an ObjectField.",
            )

        self._validate_select_field_path(bitrix_field.object_class, nested_path, original_field_path)

    def _get_field_paths_by_attr_name(self, field_paths: Iterable[Text]) -> Dict[Text, Tuple[Text, ...]]:
        """Return field paths grouped by their first attribute name."""

        grouped_paths: Dict[Text, List[Text]] = {}

        for field_path in field_paths:
            attr_name, _, nested_path = field_path.partition(".")
            nested_paths = grouped_paths.setdefault(attr_name, [])

            if nested_path:
                nested_paths.append(nested_path)

        return {
            attr_name: tuple(nested_paths)
            for attr_name, nested_paths in grouped_paths.items()
        }

    def _with_api_wrapper(self, api_wrapper: Callable[["ClientType"], Callable[..., "BitrixAPIValuesRequest[Any, BOT]"]]) -> Self:
        """Return a manager copy using another API wrapper."""
        return self._clone(api_wrapper=api_wrapper)

    def _with_params(self, **kwargs: Any) -> Self:
        """Return a manager copy with additional top-level request parameters."""

        if not kwargs:
            raise ValueError("Pass at least one request parameter.")

        current_kwargs = self._query_state.kwargs
        request_kwargs = {} if current_kwargs is None else dict(current_kwargs)
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

        order_param = self._query_state.order_param

        if not self._is_reversed:
            return order_param

        if not order_param:
            return dict.fromkeys(self._meta.pk_bitrix_codes, "DESC")

        return {
            bitrix_code: "ASC" if direction == "DESC" else "DESC"
            for bitrix_code, direction in order_param.items()
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

        kwargs = self._query_state.kwargs
        params = {} if kwargs is None else dict(kwargs)

        self._add_filter_param(params)
        self._add_order_param(params)
        self._add_select_param(params)
        self._add_start_param(params)

        return params

    def _add_filter_param(self, params: JSONDict):
        """Add filtering parameters to top-level Bitrix24 request parameters."""

        filter_param = self._query_state.filter_param

        if filter_param is None:
            return

        if self._FILTER_KEY is None:
            params.update(filter_param)
        else:
            params[self._FILTER_KEY] = dict(filter_param)

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

        state_select_param = self._query_state.select_param

        if state_select_param is None:
            return

        select_param = list(state_select_param)

        for bitrix_code in self._meta.pk_bitrix_codes:
            if bitrix_code not in select_param:
                select_param.append(bitrix_code)

        for bitrix_code in self._get_select_related_bitrix_codes():
            if bitrix_code not in select_param:
                select_param.append(bitrix_code)

        params[self._SELECT_KEY] = select_param

    def _add_start_param(self, params: JSONDict):
        """Add Bitrix24 pagination start offset to top-level request parameters."""

        if self._start_param is not None:
            if self._is_fast:
                raise BitrixObjectError("Fast list loading does not support start offset.")

            params["start"] = self._start_param

    def _get_select_related_bitrix_codes(self) -> Iterable[Text]:
        """Return source Bitrix24 field codes required by ``select_related``."""

        for field_path in self._query_state.select_related_param or ():
            yield self._meta.get_field(field_path).bitrix_code

    def _load_select_related(self, bitrix_objects: BitrixObjectList[BOT]):
        """Load configured related object fields for the supplied objects."""

        select_related_param = self._query_state.select_related_param

        if select_related_param is None:
            return

        self._load_select_related_paths(
            self._get_object_class(),
            bitrix_objects,
            select_related_param,
            self._query_state.select_field_param or {},
        )

    def _load_select_related_paths(
            self,
            object_class: "Type[BaseObject[Any]]",
            bitrix_objects: Iterable[Any],
            field_paths: Mapping[Text, Tuple[Text, ...]],
            select_fields: Mapping[Text, Tuple[Text, ...]],
    ):
        """Load related objects for one object class and optional nested paths."""

        bitrix_objects_list = list(bitrix_objects)

        for attr_name, nested_paths in field_paths.items():
            object_field = cast(ObjectField[Any], object_class.get_meta().get_field(attr_name))
            related_select_fields = select_fields.get(attr_name, ())
            related_objects = self._load_object_field_values(
                bitrix_objects_list,
                attr_name,
                object_field,
                related_select_fields,
            )

            if nested_paths:
                self._load_select_related_paths(
                    object_field.object_class,
                    related_objects,
                    self._get_field_paths_by_attr_name(nested_paths),
                    self._get_field_paths_by_attr_name(related_select_fields),
                )

    def _load_object_field_values(
            self,
            bitrix_objects: Iterable[Any],
            attr_name: Text,
            object_field: ObjectField[Any],
            select_fields: Iterable[Text],
    ) -> BitrixObjectList[Any]:
        """Load one related object field and fill already created object values."""

        bitrix_objects = list(bitrix_objects)
        unique_pks: List[Hashable] = []
        unique_pks_set = set()

        for bitrix_object in bitrix_objects:
            related_value = getattr(bitrix_object, attr_name)

            if related_value is None:
                continue

            related_objects = related_value if object_field.is_multiple else (related_value,)

            for related_object in related_objects:
                if related_object.bitrix_pk in unique_pks_set:
                    continue

                unique_pks_set.add(related_object.bitrix_pk)
                unique_pks.append(related_object.bitrix_pk)

        related_by_pk = self._load_related_objects_by_pks(object_field, unique_pks, select_fields)
        related_result = BitrixObjectList(client_provider=self._client_provider)

        for bitrix_object in bitrix_objects:
            related_value = getattr(bitrix_object, attr_name)

            if related_value is None:
                continue

            related_objects = related_value if object_field.is_multiple else (related_value,)

            for related_object in related_objects:
                loaded_object = related_by_pk.get(related_object.bitrix_pk)

                if loaded_object is not None:
                    related_object.set_bitrix_data(
                        getattr(loaded_object, "_bitrix_data"),
                        clear_local_data=False,
                        copy_data=False,
                    )

                related_result.append(related_object)

        return related_result

    def _load_related_objects_by_pks(
            self,
            object_field: ObjectField[Any],
            unique_pks: List[Hashable],
            select_fields: Iterable[Text],
    ) -> Dict[Hashable, Any]:
        """Return loaded related objects indexed by primary key."""

        related_class = object_field.object_class
        related_by_pk = {}

        if not unique_pks:
            return related_by_pk

        related_manager = related_class.objects.using(client=self._client)
        from_pks = getattr(related_manager, "from_pks", None)

        if from_pks is None:
            raise BitrixObjectError(
                f"{related_class.__name__} manager does not support from_pks(), "
                "so it cannot be preloaded through select_related(). "
                "This usually means the related object does not expose a primary-key filter field.",
            )

        related_manager = from_pks(unique_pks)

        if select_fields:
            select = getattr(related_manager, "select", None)

            if select is None:
                raise BitrixObjectError(
                    f"{related_class.__name__} manager does not support select(), "
                    "so nested fields cannot be selected through select_related().",
                )

            related_manager = select(*select_fields)

        related_objects = related_manager.all()

        for related_object in related_objects:
            related_by_pk[related_object.bitrix_pk] = related_object

        return related_by_pk

    def _make_request(self) -> "BitrixAPIValuesRequest[Any, BOT]":
        """Create a lazy values request for the current query."""

        if not self._is_result_query:
            raise TypeError(
                "Object manager has no result query. "
                "Call a query method before accessing results.",
            )

        api_wrapper_resolver = self._get_api_wrapper if self._api_wrapper is None else self._api_wrapper
        api_wrapper = api_wrapper_resolver(self._client)

        return api_wrapper(**self._get_params(), timeout=self._timeout)

    def _make_list_request(self) -> Union["BitrixAPIValuesListRequest[BOT]", "BitrixAPIValuesListFastRequest[BOT]"]:
        """Create a lazy values-list request for the current query."""

        request = self._make_request()

        if self._is_fast:
            return request.as_list_fast(
                descending=self._fast_descending,
                limit=self._limit_param,
            )
        else:
            return request.as_list(limit=self._limit_param)

