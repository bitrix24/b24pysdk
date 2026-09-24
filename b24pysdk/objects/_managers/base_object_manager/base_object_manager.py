from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, Generator, Generic, Hashable, Iterable, Iterator, List, Mapping, Optional, Sequence, Text, Tuple, Type, Union

from ...._config import Config
from ....utils.type_vars import BOT
from ....utils.types import B24APIResult, DefaultTimeout, JSONDict, Self, Timeout, cast
from ..._client_provider import ClientProvider
from ..._fields.object_field import ObjectField
from ..._filter_lookups import FilterLookup
from ..._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult, BitrixObjectList
from ...errors import BitrixObjectError, BitrixObjectFieldError, BitrixObjectFilterError
from .._base_manager import BaseManager
from ._object_query_state import ObjectQueryState, SelectParam

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
        """Initialize an unbound descriptor or a bound manager clone.

        Concrete object classes normally declare one unbound manager as a class
        attribute. Descriptor access and query-builder methods then create
        short-lived clones with an object class, client provider, and query
        state. A response is deliberately never copied into a clone: every
        distinct manager evaluates and caches its own query.
        """

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

    def __len__(self) -> int:
        """Return the result length without rematerializing an existing list.

        If this manager already owns a materialized ``BitrixObjectList``, its
        in-memory length is authoritative and no API call is made. Otherwise,
        ``count()`` is used; it ignores a pagination ``start`` but respects the
        manager's ``limit``. A cached fast-mode generator is not consumed here.
        """

        if isinstance(self._response, BitrixObjectList):
            return self._response.length

        if self._is_fast:
            raise TypeError(
                "Length is unavailable for a non-materialized fast manager. "
                "Use count() or materialize it with to_list().",
            )

        return self.count()

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
        """Return the cached response, evaluating the current query once.

        Normal list loading yields a reusable ``BitrixObjectList``. Fast mode
        may yield a one-pass generator, which remains one-pass when cached.
        ``select_related()`` needs to inspect all parent objects more than once,
        so a fast response is materialized before related values are loaded.

        The resulting list or generator is stored on this manager only. Query
        clones never share response caches, even when they share immutable query
        state.
        """

        if self._response is None:
            response = cast(
                Union[BitrixObjectList[BOT], Generator[BOT, None, None]],
                self._make_list_request().values,
            )

            select_related_param = self._query_state.select_related_param

            # ``None`` marks an ordinary terminal field selected on this object.
            # Only a nested mapping represents an ObjectField that must be loaded.
            if select_related_param and any(value is not None for value in select_related_param.values()):
                if not isinstance(response, BitrixObjectList):
                    response = BitrixObjectList(response, client_provider=self._client_provider)

                self._load_select_related(response)

            self._response = response

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

        response = BitrixObjectList(response, client_provider=self._client_provider)
        self._response = response

        return response

    def _add(
            self,
            add_params: Optional[JSONDict] = None,
            /,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BOT:
        """Create an object from raw Bitrix24 parameters and SDK field values."""
        return self._make_add_request(
            self._get_add_params(fields, add_params=add_params),
            timeout=timeout,
        ).response.value

    def _add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[BOT]:
        """Create multiple Bitrix24 objects through the client's batch API.

        ``objects_data`` may be a sequence or a mapping. Sequence positions and
        mapping keys are preserved only for failed items; successful add
        responses are collected into a ``BitrixObjectList`` without caller
        keys. Internal batch keys are compact strings and are translated back to
        the caller's mapping keys when errors are reported.

        Each field dictionary is converted independently by
        ``_get_add_params()``. An empty input returns an empty result without
        calling Bitrix24. The client remains responsible for splitting a large
        request collection into protocol-sized batches.

        Args:
            objects_data: Field dictionaries indexed either by sequence
                position or by caller-defined hashable keys.
            timeout: Optional timeout applied to individual requests and batch
                execution.

        Returns:
            Successful objects and errors separated into a
            ``BitrixObjectBatchAddResult``.
        """

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
        """Build an SDK object from a scalar, data mapping, or wrapper mapping.

        Bitrix24 add methods are not uniform: some return a primary key or full
        object data directly, while others wrap that value under one method-specific key.
        A mapping that already contains every primary-key field
        is treated as object data. Any other mapping must contain exactly one
        wrapper key and is unwrapped once.

        Conversion and primary-key validation errors are normalized to
        ``BitrixObjectError`` so callers receive an SDK-level error independent
        of the concrete response shape.
        """

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
        """Materialize target objects with the smallest supported payload.

        Bulk update and delete requests need only object primary keys. If the
        concrete manager exposes public ``select()``, this method replaces the
        ordinary select tree with the primary-key fields before loading targets.
        An existing ``select_related`` tree is preserved because it is an
        independent query option. Managers whose API has no select support fall
        back to their ordinary list representation.
        """

        if hasattr(self, "select"):
            return self._clone(
                query_state=self._query_state.with_select_param(
                    dict.fromkeys(self._meta.pk_bitrix_codes),
                ),
            ).to_list()

        return self.to_list()

    def _update(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BitrixObjectBatchWriteResult[BOT]:
        """Load matching objects and batch-update fields that remain writable."""

        if not fields:
            raise ValueError("Pass at least one field to update.")

        updated_data: JSONDict = {}

        for attr_name, value in fields.items():
            bitrix_field = self._meta.get_field(attr_name)
            bitrix_field.check_is_updatable()
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
        """Return the filtered object count, capped by ``limit``.

        ``start`` is an explicit page-position control, not part of the logical
        filter, and is therefore removed for counting. A warning is emitted when
        this happens. The method prefers Bitrix24's response ``total`` and falls
        back to the number of returned values for endpoints that omit it.

        The limit is applied locally to the total and ``start`` never reduces
        the count. ``__len__`` bypasses this request when this manager already
        has a materialized ``BitrixObjectList``.
        """

        query_state = self._query_state

        if self._start_param is not None:
            Config().logger.warning(
                "count() ignores start when counting objects matching the current filters",
                context={
                    "object_class": self._meta.object_class.__name__,
                    "start": self._start_param,
                },
            )
            query_state = query_state.with_start_param(None)

        request = self._clone(query_state=query_state)._make_request()
        total = request.response.total
        count = len(request.values) if total is None else total

        return count if self._limit_param is None else min(count, self._limit_param)

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
        """Return a manager clone with raw and SDK-style filters merged.

        ``filter_params`` is an escape hatch for endpoint-specific Bitrix24
        parameters. Keyword filters use SDK attribute names and an optional
        ``__lookup`` suffix, and are validated and converted by
        ``_get_filter_items()``. Existing filters are shallow-copied before the
        merge, preserving earlier managers in a chained query.
        """

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
    ) -> Tuple[Tuple[Text, Any], ...]:
        """Translate one SDK filter into Bitrix24 request key/value pairs.

        The synthetic ``bitrix_pk`` name expands to every field of a composite
        primary key for equality. Explicit lookups on ``bitrix_pk`` require a
        single primary-key field. Values are converted by the field and its
        lookup operator, keeping filtering rules consistent with descriptor
        assignment.

        A plain filter on a multiple field accepts either one public item value
        or an iterable of item values. One item is converted as an exact filter
        value without an operator prefix. An iterable is treated as an implicit
        ``IN`` lookup, making ``filter(tags=[1, 2])`` equivalent to
        ``filter(tags__in=[1, 2])``.

        Endpoints with ``_FILTER_KEY = None`` place filters at the top request
        level. Among explicit lookups, such endpoints support only ``in`` and
        receive its prepared iterable value without Bitrix24's ``@`` key prefix.

        Returns:
            A tuple of request items. Multiple items are possible only when a
            composite primary key is expanded.

        Raises:
            BitrixObjectFilterError: If the lookup or endpoint combination is
                unsupported.
        """

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
            if bitrix_field.is_multiple and bitrix_field.is_iterable(value):
                filter_lookup = FilterLookup.IN
            else:
                if bitrix_field.is_multiple and value is not None:
                    # Descriptor conversion normally treats a multiple field as
                    # one complete list. Wrap one filter item temporarily so it
                    # still passes through the field's public conversion path.
                    converted_values = bitrix_field.to_bitrix_value([value])

                    if not (isinstance(converted_values, list) and len(converted_values) == 1):
                        raise BitrixObjectFilterError(
                            f"Field {bitrix_field.attr_name!r} could not convert "
                            "a single multiple-field filter value.",
                        )

                    bitrix_value = converted_values[0]
                else:
                    bitrix_value = bitrix_field.to_bitrix_value(value)

                return (
                    (filter_key, bitrix_value),
                )

        if self._FILTER_KEY is None and filter_lookup is not FilterLookup.IN:
            raise BitrixObjectFilterError(
                "List methods without a dedicated filter parameter support "
                "only the 'in' filter lookup.",
            )

        object_class = self._meta.object_class

        if not object_class.supports_filter_lookup(filter_lookup):
            raise BitrixObjectFilterError(
                f"{object_class.__name__} does not support filter lookup {filter_lookup.value!r}.",
            )

        filter_operator = bitrix_field.get_filter_operator(filter_lookup)
        filter_prefix = "" if self._FILTER_KEY is None else filter_operator.bitrix_prefix

        return (
            (
                f"{filter_prefix}{filter_key}",
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
        """Return a manager clone with SDK attribute paths added to ``select``.

        Paths are validated and translated to the recursive Bitrix-code tree in
        ``ObjectQueryState`` immediately. Nested paths may cross
        ``ObjectField`` relations; their nested selections are later passed to
        the related manager by ``select_related()`` loading.
        """

        if not fields:
            raise ValueError("Pass at least one select field.")

        return self._clone(
            query_state=self._query_state.with_updated_select_param(self._get_object_class(), fields),
        )

    def _select_all(self) -> Self:
        """Return a manager clone selecting every registered concrete field.

        Existing nested selections are preserved so calling ``_select_all()``
        after selecting related-object paths does not discard their nested
        selection trees.
        """

        select_param: SelectParam = dict.fromkeys(self._meta.bitrix_codes)
        current_select_param = self._query_state.select_param

        if current_select_param is not None:
            select_param.update(current_select_param)

        return self._clone(
            query_state=self._query_state.with_select_param(select_param),
        )

    def _from_pks(self, bitrix_pks: Iterable[Hashable]) -> Self:
        """Return a manager filtered by an iterable of primary keys.

        This is the protected implementation behind a concrete manager's public
        ``from_pks()`` method and is also the contract used by
        ``select_related()``. It creates one ``IN`` filter; it never falls back
        to one request per primary key.
        """

        if isinstance(bitrix_pks, (str, bytes, bytearray)):
            raise TypeError("Primary keys must be passed as a non-string iterable.")

        return self._filter(bitrix_pk__in=bitrix_pks)

    def select_related(self, *fields: Text) -> Self:
        """Return a manager clone that preloads related object paths.

        Every non-terminal path segment must resolve to an ``ObjectField``. A
        terminal ``ObjectField`` preloads that relation with its default fields;
        a terminal ordinary field is passed as a nested selection to the nearest
        related manager. Evaluation first loads parent rows, then collects unique
        related primary keys and invokes the related manager's public
        ``from_pks()`` method. Nested relation paths are evaluated recursively.

        Missing related rows are tolerated: the original primary-key-only
        placeholder remains cached on the parent object. A relation whose
        manager has no callable ``from_pks()`` fails with ``BitrixObjectError``
        instead of issuing per-primary-key requests. Requesting terminal
        ordinary fields also requires public ``select()`` on that related
        manager, but not on the parent manager.
        """

        if not fields:
            raise ValueError("Pass at least one related field.")

        return self._clone(
            query_state=self._query_state.with_updated_select_related_param(self._get_object_class(), fields),
        )

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

    def _get_add_params(
            self,
            fields: JSONDict,
            *,
            add_params: Optional[JSONDict] = None,
    ) -> JSONDict:
        """Return add parameters built from raw codes and SDK field values.

        ``fields_params`` accepts endpoint-specific fields keyed by their raw
        Bitrix24 codes. Values supplied through SDK attribute names are
        converted normally and override matching raw codes.
        """

        if not add_params and not fields:
            raise ValueError("Pass at least one field to add.")

        # Copy raw parameters so normalizing SDK fields cannot mutate caller data.
        add_fields: JSONDict = {} if add_params is None else dict(add_params)

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

        request_params = {
            **params,
            **self._meta.required_class_params,
        }

        return self._get_add_api_wrapper(self._client)(**request_params, timeout=timeout)

    def _clone(
            self,
            *,
            object_class: Optional[Type[BOT]] = None,
            client_provider: Optional[ClientProvider] = None,
            api_wrapper: Optional[Callable[["ClientType"], Callable[..., "BitrixAPIValuesRequest[Any, BOT]"]]] = None,
            query_state: Optional[ObjectQueryState] = None,
    ) -> Self:
        """Return an unevaluated manager with selected components replaced.

        Unchanged providers, wrappers, and query state are shared by reference;
        all are read-only by convention after attachment. The response cache is
        intentionally reset by construction so evaluating one clone cannot
        affect iteration of another.
        """
        return self.__class__(
            object_class=self._object_class if object_class is None else object_class,
            client_provider=self._client_provider if client_provider is None else client_provider,
            api_wrapper=self._api_wrapper if api_wrapper is None else api_wrapper,
            query_state=self._query_state if query_state is None else query_state,
        )

    def _get_order_param(self) -> Optional[JSONDict]:
        """Return effective ordering after applying ``reverse()``.

        Reversal never mutates the stored order mapping. If no explicit order
        exists, primary-key fields are used in descending order so ``last()``
        still has deterministic semantics.
        """

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
        """Validate fast-mode ordering and return its traversal direction.

        Fast pagination can advance only through the complete primary key and
        all primary-key components must use the same direction. No ordering
        means ascending traversal. Any non-PK, partial, or mixed-direction order
        is rejected before the request is converted to a fast list.
        """

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
        """Build top-level Bitrix24 parameters for the current query state.

        A fresh top-level dictionary is always returned. Existing ``kwargs``
        are shallow-copied, then the object's fixed class parameters are applied
        so callers cannot override them. Endpoints with dedicated filter and
        order keys attach those nested mappings by reference; endpoints without
        such keys merge their entries into the fresh top-level mapping. No deep
        copy is made because query state and API request parameters treat values
        as read-only. The select list is newly materialized because primary-key
        and relation source fields may need to be appended.
        """

        kwargs = self._query_state.kwargs
        params = {
            **({} if kwargs is None else kwargs),
            **self._meta.required_class_params,
        }

        self._add_filter_param(params)
        self._add_order_param(params)
        self._add_select_param(params)
        self._add_start_param(params)

        return params

    def _add_filter_param(self, params: JSONDict):
        """Attach read-only filters using the endpoint's expected shape.

        With a dedicated filter key, the stored mapping is attached by reference.
        Otherwise, its entries are merged into the fresh top-level parameters.
        Neither path deep-copies values; downstream API request code must treat
        them as read-only, just as the manager does.
        """

        filter_param = self._query_state.filter_param

        if filter_param is None:
            return

        if self._FILTER_KEY is None:
            params.update(filter_param)
        else:
            params[self._FILTER_KEY] = filter_param

    def _add_order_param(self, params: JSONDict):
        """Attach effective ordering unless fast pagination owns the order.

        With a dedicated order key, the effective mapping is attached by
        reference; otherwise its entries are merged into the fresh top-level
        parameters. It must remain read-only downstream. Reversal produces a
        new mapping in ``_get_order_param()``.
        """

        if self._is_fast:
            return

        order_param = self._get_order_param()

        if order_param is None:
            return

        if self._ORDER_KEY is None:
            params.update(order_param)
        else:
            params[self._ORDER_KEY] = order_param

    def _add_select_param(self, params: JSONDict):
        """Attach the effective top-level Bitrix24 select list when required.

        Nested mappings are consumed only while loading related managers. A
        primary key is added after the explicit fields because every returned
        row must remain constructible as an SDK object.
        """

        state_select_param = self._query_state.select_param
        select_param = [] if state_select_param is None else list(state_select_param)
        select_related_param = self._query_state.select_related_param

        # An explicit select replaces the endpoint's default payload, so relation
        # source fields must be restored. An incomplete default payload needs the
        # same treatment even when the caller did not use select() explicitly.
        must_select_relations = state_select_param is not None or not self._meta.is_complete_without_select

        # ``None`` belongs to this endpoint and is always selected. A nested
        # mapping belongs to another object and contributes only its source ID
        # when the default response cannot be relied on.
        for bitrix_code, nested_select_related_param in (select_related_param or {}).items():
            if (nested_select_related_param is None or must_select_relations) and bitrix_code not in select_param:
                select_param.append(bitrix_code)

        if not select_param:
            return

        if not callable(getattr(self, "select", None)):
            raise BitrixObjectError(
                f"Cannot select {self._get_object_class().__name__} fields {tuple(select_param)!r}: "
                f"{self.__class__.__name__} does not support select().",
            )

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

    def _load_select_related(self, bitrix_objects: BitrixObjectList[BOT]):  # noqa: C901
        """Resolve and cache all configured relations for materialized parents.

        Loading is performed once per selected relation at the current object
        level. The method collects unique primary keys from all parents, creates
        one related-manager ``from_pks()`` query, and builds a primary-key index
        from its result. That related manager receives the nested ordinary
        select tree and nested ``select_related`` tree, so deeper relations are
        handled recursively by the same mechanism.

        A second parent pass replaces primary-key-only placeholders with loaded
        objects. For multiple relations, the already cached
        ``BitrixObjectList`` is updated in place to avoid copying it. A related
        row omitted by Bitrix24 is not an error: its original placeholder is
        retained. The second descriptor read is served by ``ObjectField``'s
        cache and does not reload parent data.

        For one relation, work is linear in parent objects, relation references,
        and returned related objects. Temporary memory consists of unique keys
        and the related-object index; no cache outlives the parent objects except
        the related values intentionally stored by their field descriptors.

        Args:
            bitrix_objects: Fully materialized parent objects to enrich in
                place.

        Raises:
            BitrixObjectError: If a related manager lacks public ``from_pks()``
                support or cannot apply a requested nested ``select()``.
        """

        select_related_param = self._query_state.select_related_param

        if select_related_param is None:
            return

        def load_related_objects_by_pks(
            object_field: ObjectField[Any],
            unique_pks: List[Hashable],
            related_select_param: Optional[SelectParam],
            nested_select_related_param: Optional[SelectParam],
        ) -> Dict[Hashable, Any]:
            """Load unique related keys and index returned objects by key.

            Empty key collections short-circuit without resolving the related
            manager or making an API request. A single fast manager query is
            used for all keys, allowing the API layer to split explicit IDs
            into independent requests without last-ID pagination.
            """

            if not unique_pks:
                return {}

            related_class = object_field.object_class

            related_manager = related_class.objects.using(client=self._client)

            if self._timeout is not None:
                related_manager = related_manager.timeout(self._timeout)

            from_pks: Optional[Callable[[Iterable[Hashable]], "BaseObjectManager[Any]"]] = getattr(related_manager, "from_pks", None)

            if not callable(from_pks):
                raise BitrixObjectError(
                    f"Cannot preload {self._get_object_class().__name__}.{object_field.attr_name}: "
                    f"{related_class.__name__} manager does not support filtering "
                    "by primary keys via from_pks().",
                )

            related_manager = from_pks(unique_pks).as_fast()
            related_query_state = related_manager._query_state

            # Explicit select() state and select_related() state stay separate:
            # their top-level fields follow different request inclusion rules.
            if related_select_param is not None:
                related_query_state = related_query_state.with_select_param(related_select_param)

            if nested_select_related_param is not None:
                related_query_state = related_query_state.with_select_related_param(nested_select_related_param)

            related_objects = related_manager._clone(query_state=related_query_state)

            return {
                related_object.bitrix_pk: related_object
                for related_object in related_objects
            }

        def load_object_field_values(
                object_field: ObjectField[Any],
                related_select_param: Optional[SelectParam],
                nested_select_related_param: Optional[SelectParam],
        ):
            """Collect, load, and cache values for one selected object field."""

            unique_pks: List[Hashable] = []
            unique_pks_set = set()

            # Preserve first-seen order for deterministic request parameters
            # while the companion set keeps duplicate checks constant-time.
            for bitrix_object in bitrix_objects:
                related_value = getattr(bitrix_object, object_field.attr_name)

                if related_value is None:
                    continue

                related_objects = related_value if object_field.is_multiple else (related_value,)

                for related_object in related_objects:
                    if related_object.bitrix_pk in unique_pks_set:
                        continue

                    unique_pks_set.add(related_object.bitrix_pk)
                    unique_pks.append(related_object.bitrix_pk)

            related_by_pk = load_related_objects_by_pks(
                object_field,
                unique_pks,
                related_select_param,
                nested_select_related_param,
            )

            # Descriptor reads hit the values cached during the first pass. For
            # multiple relations, mutate that same list instead of allocating a
            # replacement with identical shape.
            for bitrix_object in bitrix_objects:
                related_value = getattr(bitrix_object, object_field.attr_name)

                if related_value is None:
                    continue

                if object_field.is_multiple:
                    for index, related_object in enumerate(related_value):
                        related_value[index] = related_by_pk.get(
                            related_object.bitrix_pk,
                            related_object,
                        )

                    loaded_value = related_value
                else:
                    loaded_value = related_by_pk.get(related_value.bitrix_pk, related_value)

                object_field.set_cached_value(bitrix_object, loaded_value)

        select_param = self._query_state.select_param

        for bitrix_code, selected_nested_select_related_param in select_related_param.items():
            # Terminal ordinary fields were already handled by _add_select_param().
            # Only nested mappings describe relations that require another query.
            if selected_nested_select_related_param is None:
                continue

            selected_object_field = self._meta.get_object_field_by_bitrix_code(bitrix_code)
            selected_related_param = None if select_param is None else select_param.get(bitrix_code)
            load_object_field_values(
                selected_object_field,
                selected_related_param,
                selected_nested_select_related_param,
            )

    def _make_request(self) -> "BitrixAPIValuesRequest[Any, BOT]":
        """Create, but do not explicitly evaluate, the current API request.

        The manager must first have been turned into a result query by a query
        method such as ``all()``, ``filter()``, or ``limit()``. A custom wrapper
        takes precedence over the concrete manager's default resolver.
        """

        if not self._is_result_query:
            raise TypeError(
                "Object manager has no result query. "
                "Call a query method before accessing results.",
            )

        api_wrapper_resolver = self._get_api_wrapper if self._api_wrapper is None else self._api_wrapper
        api_wrapper = api_wrapper_resolver(self._client)

        return api_wrapper(**self._get_params(), timeout=self._timeout)

    def _make_list_request(self) -> Union["BitrixAPIValuesListRequest[BOT]", "BitrixAPIValuesListFastRequest[BOT]"]:
        """Adapt the current request to normal or fast list loading.

        Normal mode delegates pagination and the optional limit to ``as_list``.
        Fast mode delegates keyset traversal direction and may expose a one-pass
        generator through the returned request's ``values`` property.
        """

        request = self._make_request()

        if self._is_fast:
            return request.as_list_fast(descending=self._fast_descending, limit=self._limit_param)
        else:
            return request.as_list(limit=self._limit_param)
