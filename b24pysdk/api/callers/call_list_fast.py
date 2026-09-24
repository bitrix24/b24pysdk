from datetime import datetime
from typing import Callable, Dict, Final, Iterable, List, Literal, Optional, Text, Tuple, Union

from ...constants.version import B24APIVersion
from ...protocols import BitrixTokenProtocol
from ...schemas.api import BatchResponseData, BatchResultData, ListFastResponseData, ResponseData, TimeResponseData
from ...utils.types import B24APIVersionLiteral, B24RequestTuple, JSONDict, JSONGenerator, JSONList, Timeout, cast
from ._base_list_caller import BaseListCaller
from ._utils import get_empty_time
from .call_batch import call_batch
from .call_method import call_method

__all__ = [
    "call_list_fast",
]


class _ListFastCaller(BaseListCaller):
    """
    Caller for fast classic list retrieval without total counting.

    For an unknown result set, the caller uses a moving ID window whose batch
    filters depend on the last ID returned by the preceding page. When the
    request filters only by explicit IDs, it skips that pagination chain and
    sends independent ID chunks instead. Both strategies order results by an
    ID-like field and use ``start=-1`` to disable total calculation.
    """

    _DEFAULT_ID_FIELD: Final[Text] = "ID"
    _DEFAULT_FILTER_PATTERN: Final[Callable[[Text, Union[int, Text]], JSONDict]] = staticmethod(
        lambda filter_key, filter_value: {"filter": {filter_key: filter_value}},
    )
    _DEFAULT_ORDER_PATTERN: Final[Callable[[Text, Text], JSONDict]] = staticmethod(
        lambda id_field, sorting: {"order": {id_field: sorting}},
    )
    _MANAGED_PARAMS: Final[Tuple[Text, ...]] = ("order", "sort", "start")
    _START: Final[int] = -1

    _REQUEST_ID_FIELDS: Final[Dict[Text, Text]] = {
        "crm.automatedsolution": "id",
        "crm.type": "id",
        "socialnetwork.api.workgroup": "ID",
        "tasks.task": "ID",
    }

    _ORDER_PATTERNS: Final[Dict[Text, Callable[[Text, Text], JSONDict]]] = {
        "department": lambda id_field, sorting: {"SORT": id_field, "ORDER": sorting},
        "user": lambda id_field, sorting: {"SORT": id_field, "ORDER": sorting},
        "user.userfield": lambda id_field, sorting: {"order": {id_field: sorting}},
    }

    _FILTER_PATTERNS: Final[Dict[Text, Callable[[Text, Union[int, Text]], JSONDict]]] = {
        "department": lambda filter_key, filter_value: {filter_key: filter_value},
    }

    __slots__ = (
        "_counter",
        "_descending",
        "_filter_pattern",
        "_last_id",
        "_limit",
        "_now_datetime",
        "_order_pattern",
        "_request_id_field",
        "_response_id_field",
        "_results",
        "_time",
        "_wrapper",
    )

    _descending: bool
    _limit: Optional[int]
    _now_datetime: datetime
    _time: TimeResponseData
    _counter: int
    _last_id: int
    _request_id_field: Optional[Text]
    _response_id_field: Optional[Text]
    _wrapper: Optional[Text]
    _filter_pattern: Callable[[Text, Union[int, Text]], JSONDict]
    _order_pattern: Callable[[Text, Text], JSONDict]
    _results: Optional[Union[JSONDict, JSONList]]

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            api_method: Text,
            params: Optional[JSONDict] = None,
            descending: bool = False,
            limit: Optional[int] = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            bitrix_token: Optional[BitrixTokenProtocol] = None,
            **kwargs,
    ):
        """
        Initialize fast list retrieval state.

        Args:
            domain: Bitrix24 portal domain.
            auth_token: OAuth access token or webhook token.
            is_webhook: Whether ``auth_token`` is a webhook token.
            api_method: List-like REST method name.
            params: Base method parameters. ``order``, ``sort``, and ``start``
                must not be passed because this caller manages them internally.
            descending: Retrieve items by descending ID-like field when ``True``.
            limit: Maximum number of yielded items, or ``None`` for all items.
            prefer_version: Preferred API version. V3 methods are rejected
                because this caller uses classic filtering and batch syntax.
            bitrix_token: Optional token wrapper used for retry/refresh logic.
            **kwargs: Extra requester options forwarded to lower-level calls.
        """
        super().__init__(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=api_method,
            params=params,
            prefer_version=prefer_version,
            bitrix_token=bitrix_token,
            **kwargs,
        )
        if self._api_version == B24APIVersion.V3:
            raise TypeError("Bitrix API v3 methods are not supported by call_list_fast yet.")

        managed_params = tuple(
            key
            for key in self._params
            if key.lower() in self._MANAGED_PARAMS
        )

        if managed_params:
            raise ValueError(
                "Parameters managed internally by call_list_fast cannot be passed in params: "
                f"{', '.join(map(repr, managed_params))}.",
            )

        self._descending = descending
        self._limit = limit
        self._now_datetime = self._config.get_local_datetime()
        self._time = get_empty_time(self._now_datetime)
        self._counter = 0
        self._last_id = 0
        self._request_id_field = self._get_initial_request_id_field()
        self._response_id_field = None
        self._wrapper = None
        self._filter_pattern = self._get_filter_pattern()
        self._order_pattern = self._get_order_pattern()
        self._results = None

    def _get_initial_request_id_field(self) -> Optional[Text]:
        """
        Resolve the request-side ID field configured for the current method.

        Some methods use lower-case or method-specific ID field names. The
        lookup first tries the full method name and then progressively trims
        suffixes, allowing family-level configuration such as ``crm.type``.
        """

        api_method = self._api_method
        request_id_field = self._REQUEST_ID_FIELDS.get(api_method)

        while not (api_method.find(".") == -1 or request_id_field):
            api_method, _ = api_method.rsplit(".", maxsplit=1)
            request_id_field = self._REQUEST_ID_FIELDS.get(api_method)

        return request_id_field

    def _get_order_pattern(self) -> Callable[[Text, Text], JSONDict]:
        """
        Resolve how the current method expresses sorting by ID.

        Most methods use ``{"order": {id_field: sorting}}``. A few older
        methods use top-level ``SORT``/``ORDER`` parameters, so this method
        selects the proper pattern for the API method family.
        """

        api_method = self._api_method
        order_pattern = self._ORDER_PATTERNS.get(api_method)

        while not (api_method.find(".") == -1 or order_pattern):
            api_method, _ = api_method.rsplit(".", maxsplit=1)
            order_pattern = self._ORDER_PATTERNS.get(api_method)

        return order_pattern or self._DEFAULT_ORDER_PATTERN

    def _get_filter_pattern(self) -> Callable[[Text, Union[int, Text]], JSONDict]:
        """
        Resolve how the current method expresses a dynamic ID filter.

        Most list methods place comparison filters inside ``filter``. A few
        older methods, such as ``department.get``, accept filter fields at the
        top request level, so their moving ID boundary must use the same shape.
        """

        api_method = self._api_method
        filter_pattern = self._FILTER_PATTERNS.get(api_method)

        while not (api_method.find(".") == -1 or filter_pattern):
            api_method, _ = api_method.rsplit(".", maxsplit=1)
            filter_pattern = self._FILTER_PATTERNS.get(api_method)

        return filter_pattern or self._DEFAULT_FILTER_PATTERN

    @property
    def _cmp(self) -> Literal[">", "<"]:
        """Return the comparison operator used to advance the ID window."""
        return "<" if self._descending else ">"

    @property
    def _dynamic_request_id_field(self) -> Text:
        """
        Return the ID field name used in generated request filters.

        Preference order is explicit method configuration, then the ID field
        detected from the first response, then the default ``ID`` field.
        """
        return self._request_id_field or self._response_id_field or self._DEFAULT_ID_FIELD

    @property
    def _filter_key(self) -> Text:
        """Return the Bitrix filter key for the moving ID boundary."""
        return f"{self._cmp}{self._dynamic_request_id_field}"

    @property
    def _sorting(self) -> Literal["ASC", "DESC"]:
        """Return Bitrix sort direction matching the requested traversal order."""
        return "DESC" if self._descending else "ASC"

    @property
    def _order_by_id(self) -> JSONDict:
        """Return ordering parameters for the current ID field and direction."""
        return self._order_pattern(self._dynamic_request_id_field, self._sorting)

    @staticmethod
    def _force_values(collection: Union[JSONDict, JSONList]) -> Iterable[Union[JSONDict, JSONList]]:
        """Return batch values ordered by their numeric command keys."""
        if isinstance(collection, dict):
            return (collection[key] for key in sorted(collection, key=int))
        else:
            return collection

    @property
    def _results_values(self) -> Iterable[Union[JSONDict, JSONList]]:
        """Return iterable page payloads from the most recent batch result."""
        return self._force_values(self._results)

    def _deep_merge(self, *dicts: Dict) -> Dict:
        """
        Merge nested dictionaries recursively.

        Later dictionaries override earlier scalar values. Nested dictionaries
        are merged recursively so generated filter/order parameters can be
        layered on top of caller-provided parameters without discarding unrelated
        nested keys.
        """

        result_dict: Dict = {}

        for current_dict in dicts:
            for key, value in current_dict.items():
                existing_value = result_dict.get(key)

                if isinstance(value, dict):
                    if existing_value is not None and not isinstance(existing_value, dict):
                        raise ValueError(f"Cannot merge a dict into a non-dict at key '{key}': {existing_value}")

                    result_dict[key] = self._deep_merge(existing_value or {}, value)
                else:
                    result_dict[key] = value

        return result_dict

    def _add_time(self, time: TimeResponseData):
        """Accumulate Bitrix timing metadata from one method or batch response."""

        self._time["finish"] = time["finish"]
        self._time["duration"] += time["duration"]
        self._time["processing"] += time["processing"]
        self._time["date_finish"] = time["date_finish"]

        operating_reset_at = time.get("operating_reset_at")

        if operating_reset_at is not None:
            self._time["operating_reset_at"] = operating_reset_at

        operating = time.get("operating")

        if operating is not None:
            self._time["operating"] = self._time.get("operating", 0) + operating

    def _unwrap_result(self, result: Union[JSONDict, JSONList]) -> Tuple[Optional[Text], JSONList]:
        """
        Extract the list payload and remember its wrapper key.

        Bitrix list methods often return data under a wrapper such as
        ``{"items": [...]}``. The wrapper is needed later to build batch
        expressions that reference previous batch results.
        """

        wrapper = None

        while isinstance(result, dict):
            wrapper, result = next(iter(result.items()))

        if isinstance(result, list):
            return wrapper, result
        else:
            raise TypeError(f"Bitrix API method {self._api_method!r} is not a list-type method!")

    def _get_path(self, counter: int) -> Text:
        """
        Build a Bitrix batch expression pointing to the previous request result.

        The generated expression is used inside later batch commands to read the
        last item ID from the previous command and continue the moving ID window.
        """

        path = f"$result[{counter}]"

        if self._wrapper:
            path = f"{path}[{self._wrapper}]"

        return path

    def _get_filter_by_id(self, counter: int) -> JSONDict:
        """
        Generate the moving ID filter for one command in a batch chain.

        The first command uses the stored ``_last_id`` from the previous batch,
        if any. Later commands reference the previous command's last returned
        item through a Bitrix batch expression, allowing a single batch request
        to fetch several consecutive pages.
        """

        if counter == 1:
            if not self._last_id:
                return {}

            filter_value = self._last_id
        else:
            filter_value = (
                f"{self._get_path(counter - 1)}"
                f"[{self._MAX_BATCH_SIZE - 1}]"
                f"[{self._response_id_field}]"
            )

        return self._filter_pattern(self._filter_key, filter_value)

    def _generate_method_params(self, counter: int = 1) -> JSONDict:
        """
        Build parameters for one fast-list request.

        The result merges caller parameters with generated ordering, moving-ID
        filter, and ``start=-1`` to skip total counting.
        """
        return self._deep_merge(
            self._params,
            self._order_by_id,
            self._get_filter_by_id(counter=counter),
            {"start": self._START},
        )

    def _get_batch_methods_count(self) -> int:
        """Return how many batch commands are needed for the remaining limit."""

        if self._limit is None:
            return self._MAX_BATCH_SIZE

        remaining_limit = self._limit - self._counter

        if remaining_limit <= 0:
            return 0

        methods_count = remaining_limit // self._MAX_BATCH_SIZE

        if remaining_limit % self._MAX_BATCH_SIZE:
            methods_count += 1

        return min(self._MAX_BATCH_SIZE, methods_count)

    def _generate_batch_methods(self) -> Dict[Text, B24RequestTuple]:
        """
        Generate one chain of fast-list batch commands.

        Every command uses the same API method with generated order, filter, and
        ``start=-1`` parameters. Commands use one-based string keys ``"1"``,
        ``"2"``, ... so Bitrix keeps batch results dict-shaped. Later filters
        reference preceding command results by these keys.
        The number of generated commands is limited by the remaining requested
        item count when ``limit`` is set.

        Returns:
            Dictionary of request names to ``(api_method, params)`` tuples ready
            for ``call_batch``.
        """

        methods: Dict[Text, B24RequestTuple] = {}

        for counter in range(1, self._get_batch_methods_count() + 1):
            method_params = self._generate_method_params(counter=counter)
            methods[str(counter)] = (self._api_method, method_params)

        return methods

    def _generate_filter_id_batch_methods(
            self,
            filter_key: Text,
            filter_id_key: Text,
            filter_ids: List[int],
    ) -> Dict[Text, B24RequestTuple]:
        """Generate independent ``start=-1`` commands for explicit IDs.

        Each command receives at most one Bitrix24 page of IDs and therefore
        cannot require pagination. The regular ID ordering is included in every
        command. An empty ``filter_key`` means that the API method accepts ``ID``
        directly at the top request level.

        Args:
            filter_key: Enclosing filter key, or an empty string for a
                top-level ID filter.
            filter_id_key: Actual case-preserving ``ID`` or ``@ID`` key.
            filter_ids: IDs assigned to this physical batch request.

        Returns:
            Named method commands ready for one ``call_batch`` invocation.
        """

        methods: Dict[Text, B24RequestTuple] = {}

        for counter, start in enumerate(range(0, len(filter_ids), self._MAX_BATCH_SIZE), start=1):
            id_chunk = filter_ids[start:start + self._MAX_BATCH_SIZE]
            filter_params = (
                {filter_key: {filter_id_key: id_chunk}}
                if filter_key else {filter_id_key: id_chunk}
            )
            method_params = self._deep_merge(
                self._params,
                filter_params,
                self._order_by_id,
                {"start": self._START},
            )
            methods[str(counter)] = (self._api_method, method_params)

        return methods

    def _fetch_first_response(self) -> ResponseData:
        """
        Fetch the first moving-ID page to discover wrapper and ID field names.

        Later batch commands depend on the response wrapper and ID field found
        in this initial response. The explicit ID-only strategy does not need
        this discovery request.
        """
        if self._bitrix_token:
            response = self._bitrix_token.call_method(
                api_method=self._api_method,
                params=self._generate_method_params(),
                **self._kwargs,
            )
        else:
            response = call_method(
                domain=self._domain,
                auth_token=self._auth_token,
                is_webhook=self._is_webhook,
                api_method=self._api_method,
                params=self._generate_method_params(),
                **self._kwargs,
            )

        return cast(ResponseData, response)

    def _fetch_batch_response(self, methods: Dict[Text, B24RequestTuple]) -> BatchResponseData:
        """Execute one classic batch containing the supplied commands."""
        return call_batch(
            domain=self._domain,
            auth_token=self._auth_token,
            is_webhook=self._is_webhook,
            methods=methods,
            halt=self._HALT,
            bitrix_token=self._bitrix_token,
            **self._kwargs,
        )

    def _warn_batch_result_errors(self, batch_result: BatchResultData):
        """Log warning when a batch response contains command errors."""

        result_error = batch_result.get("result_error")

        if result_error:
            self._config.logger.warning(
                "batch result contains errors",
                context={
                    "api_method": self._api_method,
                    "result_error": result_error,
                },
            )

    def _extract_response_id_field(self, result_value: JSONDict) -> Text:
        """
        Detect the actual ID key returned by Bitrix in a result item.

        The comparison is case-insensitive because different methods may return
        ``ID`` or ``id``. The detected key is reused in batch expressions.
        """

        for key in result_value:
            if key.upper() == self._DEFAULT_ID_FIELD:
                return key

        raise ValueError("ID key is not found in Bitrix responses!")

    def _update_last_id(self, new_last_id: int) -> bool:
        """
        Store the last emitted ID and guard against infinite pagination loops.

        Returns:
            ``True`` if the moving ID boundary was updated. ``False`` if Bitrix
            returned the same boundary ID again, which usually means that the
            method does not support the generated ID-window filter.
        """

        if new_last_id != self._last_id:
            self._last_id = new_last_id
            return True

        self._config.logger.info(
            "stop call_list_fast because Bitrix returned the same ID sequence",
            context={
                "api_method": self._api_method,
                "filter_key": self._filter_key,
                "last_id": self._last_id,
                "new_last_id": new_last_id,
            },
        )

        return False

    def _generate_result_by_ids(
            self,
            filter_key: Text,
            filter_id_key: Text,
            filter_ids: List[int],
    ) -> JSONGenerator:
        """Yield explicitly selected IDs through independent batch commands.

        IDs are sorted in the requested traversal direction before chunking.
        Batch command results are processed by their one-based numeric keys, while
        objects from each command are yielded immediately without accumulating an
        intermediate list. One physical batch contains at most ``MAX_BATCH_SIZE``
        commands, and every command filters at most ``MAX_BATCH_SIZE`` IDs.

        Args:
            filter_key: Enclosing filter key, or an empty string for a
                top-level ID filter.
            filter_id_key: Actual case-preserving ``ID`` or ``@ID`` key.
            filter_ids: Complete materialized collection of requested IDs.
        """

        sorted_filter_ids = sorted(filter_ids, reverse=self._descending)
        start = 0

        while start < len(sorted_filter_ids):
            methods_count = self._get_batch_methods_count()

            if not methods_count:
                return

            end = start + methods_count * self._MAX_BATCH_SIZE

            batch_response = self._fetch_batch_response(
                methods=self._generate_filter_id_batch_methods(
                    filter_key=filter_key,
                    filter_id_key=filter_id_key,
                    filter_ids=sorted_filter_ids[start:end],
                ),
            )

            start = end

            batch_result = batch_response["result"]

            self._warn_batch_result_errors(batch_result)
            self._add_time(batch_response["time"])

            for result_value in self._force_values(batch_result["result"]):
                _, unwrapped_result_values = self._unwrap_result(result_value)

                for unwrapped_result_value in unwrapped_result_values:
                    yield unwrapped_result_value
                    self._counter += 1

                    if self._limit is not None and self._counter >= self._limit:
                        return

    def _generate_paginated_result(self) -> JSONGenerator:
        """Yield an unknown result set through moving-ID pagination."""

        response = self._fetch_first_response()

        self._add_time(response["time"])
        self._wrapper, unwrapped_result_values = self._unwrap_result(response["result"])

        if unwrapped_result_values:
            self._results = [response["result"]]
        else:
            return

        self._response_id_field = self._extract_response_id_field(unwrapped_result_values[0])

        while self._results:
            for result_values in self._results_values:
                unwrapped_result_values = result_values[self._wrapper] if self._wrapper else result_values

                if not unwrapped_result_values:
                    return

                new_last_id = int(unwrapped_result_values[-1][self._response_id_field])

                if not self._update_last_id(new_last_id):
                    return

                for result_value in unwrapped_result_values:
                    yield result_value
                    self._counter += 1

                    if self._limit is not None and self._counter >= self._limit:
                        return

                if len(unwrapped_result_values) < self._MAX_BATCH_SIZE:
                    return

            batch_response = self._fetch_batch_response(methods=self._generate_batch_methods())
            batch_result = batch_response["result"]

            self._warn_batch_result_errors(batch_result)
            self._add_time(batch_response["time"])
            self._results = batch_result["result"]

    def _generate_result(self) -> JSONGenerator:
        """Select the ID-only or moving-ID strategy and yield its items."""
        try:
            if self._limit is not None and self._limit <= 0:
                return

            filter_key, filter_id_key, filter_ids = self._check_filter_by_id_only()

            if filter_ids is None:
                yield from self._generate_paginated_result()
            else:
                yield from self._generate_result_by_ids(
                    filter_key=filter_key,
                    filter_id_key=filter_id_key,
                    filter_ids=filter_ids,
                )
        finally:
            self._config.logger.debug("finish call_list_fast")

    def call(self) -> ListFastResponseData:
        """
        Return a lazy result generator and accumulated timing metadata.

        The ``result`` value is a one-time generator. Items are fetched progressively as
        the consumer iterates over it, while ``time`` is updated as pages are loaded.
        Final timing values are available only after the generator has been fully
        consumed.
        """

        self._config.logger.debug(
            "start call_list_fast",
            context={
                "descending": self._descending,
            },
        )

        return {
            "result": self._generate_result(),
            "time": self._time,
        }


def call_list_fast(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        api_method: Text,
        params: Optional[JSONDict] = None,
        descending: bool = False,
        limit: Optional[int] = None,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> ListFastResponseData:
    """
    Retrieve a large classic list result without Bitrix total counting.

    Unknown result sets use moving-ID pagination. Requests filtered only by an
    explicit ID iterable are split into independent sorted commands instead,
    avoiding both the discovery request and pagination by the last returned ID.
    Every generated method call includes ``start=-1``.

    Note:
        On small sets of items (2550 entries and less), ``call_list`` can be
        faster because it uses the classic ``total``/``next`` pagination flow.
        This helper is optimized for large V1/V2 datasets and is not compatible
        with V3 ``/rest/api`` list methods.

    Args:
        domain: Bitrix24 portal domain.
        auth_token: OAuth access token or webhook token.
        is_webhook: Whether ``auth_token`` is a webhook token.
        api_method: List-like REST method name, for example ``crm.deal.list``.
        params: Base method parameters sent to Bitrix. Must not contain
            ``order``, ``sort``, or ``start`` because this helper generates
            these parameters internally.
        descending: Retrieve items in descending ID order when ``True``.
        limit: Maximum number of items to retrieve.
        timeout: Request timeout in seconds.
        prefer_version: Preferred API version to resolve the method against.
        bitrix_token: Optional token wrapper used by nested execution.
        **kwargs: Extra requester options, such as retry configuration.

    Returns:
        BitrixAPIFastListResponse containing a lazy one-time ``result`` generator
        and a mutable ``time`` dictionary. The ``time`` dictionary is updated while
        the generator is consumed, so final timing values are available only after
        the result generator has been fully iterated.
    """
    return _ListFastCaller(
        domain=domain,
        auth_token=auth_token,
        is_webhook=is_webhook,
        api_method=api_method,
        params=params,
        descending=descending,
        limit=limit,
        timeout=timeout,
        prefer_version=prefer_version,
        bitrix_token=bitrix_token,
        **kwargs,
    ).call()
