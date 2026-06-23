from datetime import datetime
from typing import Callable, Dict, Final, Iterable, Literal, Optional, Text, Tuple, Union

from ..._constants import MAX_BATCH_SIZE
from ...constants.version import B24APIVersion
from ...protocols import BitrixTokenProtocol
from ...schemas.time import TimeData
from ...utils.types import B24APIVersionLiteral, B24RequestTuple, JSONDict, JSONGenerator, JSONList, Timeout
from ._base_caller import BaseCaller
from ._utils import get_empty_time
from .call_batch import call_batch
from .call_method import call_method

__all__ = [
    "call_list_fast",
]


class _ListFastCaller(BaseCaller):
    """
    Caller for fast classic list retrieval by moving ID window.

    Instead of relying on Bitrix ``total`` counting, this caller orders results
    by an ID-like field, disables total calculation with ``start=-1``, and uses
    batch requests whose filters depend on the last ID returned by the previous
    page. This is useful for large V1/V2 datasets where total counting is slow.
    """

    _DEFAULT_ID_FIELD: Final[Text] = "ID"
    _DEFAULT_ORDER_PATTERN: Final[Callable[[Text, Text], JSONDict]] = staticmethod(lambda id_field, sorting: {"order": {id_field: sorting}})
    _HALT: Final[bool] = True
    _MAX_BATCH_SIZE: Final[int] = MAX_BATCH_SIZE
    _START: Final[int] = -1

    _REQUEST_ID_FIELDS: Final[Dict[Text, Text]] = {
        "crm.automatedsolution": "id",
        "crm.type": "id",
        "socialnetwork.api.workgroup": "ID",
        "tasks.task": "ID",
    }

    _ORDER_PATTERNS: Final[Dict[Text, Callable[[Text, Text], JSONDict]]] = {
        "department": staticmethod(lambda id_field, sorting: {"SORT": id_field, "ORDER": sorting}),
        "user": staticmethod(lambda id_field, sorting: {"SORT": id_field, "ORDER": sorting}),
        "user.userfield": _DEFAULT_ORDER_PATTERN,
    }

    __slots__ = (
        "_counter",
        "_descending",
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
    _time: TimeData
    _counter: int
    _last_id: int
    _request_id_field: Optional[Text]
    _response_id_field: Optional[Text]
    _wrapper: Optional[Text]
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
            params: Base method parameters. They are merged with generated
                ordering, filter, and ``start=-1`` parameters.
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
        self._descending = descending
        self._limit = limit
        self._now_datetime = self._config.get_local_datetime()
        self._time = get_empty_time(self._now_datetime)
        self._counter = 0
        self._last_id = 0
        self._request_id_field = self._get_initial_request_id_field()
        self._response_id_field = None
        self._wrapper = None
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
    def _prop(self) -> Text:
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
        """Return iterable values for either dict-shaped or list-shaped results."""
        if isinstance(collection, dict):
            return collection.values()
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

    def _add_time(self, time: TimeData):
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

    def _unwrap_result(self, result: JSONDict) -> Tuple[Optional[Text], JSONList]:
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

    def _get_path(self, index: int) -> Text:
        """
        Build a Bitrix batch expression pointing to the previous request result.

        The generated expression is used inside later batch commands to read the
        last item ID from the previous command and continue the moving ID window.
        """

        path = f"$result[req_{index - 1}]"

        if self._wrapper:
            path = f"{path}[{self._wrapper}]"

        return path

    def _get_filter_by_id(self, index: int) -> JSONDict:
        """
        Generate the moving ID filter for one command in a batch chain.

        The first command uses the stored ``_last_id`` from the previous batch,
        if any. Later commands reference the previous command's last returned
        item through a Bitrix batch expression, allowing a single batch request
        to fetch several consecutive pages.
        """

        if index == 0:
            if self._last_id:
                return {
                    "filter": {
                        self._prop: self._last_id,
                    },
                }
            else:
                return {}

        return {
            "filter": {
                self._prop: f"{self._get_path(index)}[{self._MAX_BATCH_SIZE - 1}][{self._response_id_field}]",
            },
        }

    def _generate_method_params(self, index: int = 0) -> JSONDict:
        """
        Build parameters for one fast-list request.

        The result merges caller parameters with generated ordering, moving-ID
        filter, and ``start=-1`` to skip total counting.
        """
        return self._deep_merge(
            self._params,
            self._order_by_id,
            self._get_filter_by_id(index=index),
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
        ``start=-1`` parameters. Commands are named ``req_0``, ``req_1``, ...
        because later filters reference earlier command results by these names.
        The number of generated commands is limited by the remaining requested
        item count when ``limit`` is set.

        Returns:
            Dictionary of request names to ``(api_method, params)`` tuples ready
            for ``call_batch``.
        """

        methods: Dict[Text, B24RequestTuple] = {}

        for index in range(self._get_batch_methods_count()):
            method_params = self._generate_method_params(index=index)
            methods[f"req_{index}"] = (self._api_method, method_params)

        return methods

    def _fetch_first_response(self) -> JSONDict:
        """
        Fetch the first page outside batch to discover wrapper and ID field names.

        Later batch commands depend on the response wrapper and ID field found
        in this initial response.
        """
        if self._bitrix_token:
            return self._bitrix_token.call_method(
                api_method=self._api_method,
                params=self._generate_method_params(),
                **self._kwargs,
            )
        else:
            return call_method(
                domain=self._domain,
                auth_token=self._auth_token,
                is_webhook=self._is_webhook,
                api_method=self._api_method,
                params=self._generate_method_params(),
                **self._kwargs,
            )

    def _fetch_next_batch_response(self) -> JSONDict:
        """Fetch the next chain of pages through one classic batch request."""
        return call_batch(
            domain=self._domain,
            auth_token=self._auth_token,
            is_webhook=self._is_webhook,
            methods=self._generate_batch_methods(),
            halt=self._HALT,
            bitrix_token=self._bitrix_token,
            **self._kwargs,
        )

    def _warn_batch_result_errors(self, batch_result: JSONDict):
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

    def _update_last_id(self, new_last_id: int):
        """
        Store the last emitted ID and guard against infinite pagination loops.

        If Bitrix returns the same boundary ID twice, the moving filter would
        keep requesting the same page forever, so the method raises ``ValueError``.
        """
        if new_last_id != self._last_id:
            self._last_id = new_last_id
        else:
            raise ValueError(
                "Bitrix API returned the same ID sequence: "
                f"last_id={self._last_id}, new_last_id={new_last_id}. "
                "This can lead to an infinite generation loop!",
            )

    def _generate_result(self) -> JSONGenerator:
        """
        Yield items one by one while fetching additional pages as needed.

        The generator starts with a normal method call, then repeatedly requests
        chained batch pages until a short page is returned or ``limit`` is
        reached.
        """
        try:
            if self._limit is not None and self._limit <= 0:
                return

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

                    for result_value in unwrapped_result_values:
                        yield result_value
                        self._counter += 1

                        if self._limit is not None and self._counter >= self._limit:
                            return

                    if len(unwrapped_result_values) < self._MAX_BATCH_SIZE:
                        return

                if self._limit is not None and self._counter >= self._limit:
                    return

                new_last_id = int(unwrapped_result_values[-1][self._response_id_field])
                self._update_last_id(new_last_id)

                batch_response = self._fetch_next_batch_response()
                batch_result = batch_response["result"]

                self._warn_batch_result_errors(batch_result)
                self._add_time(batch_response["time"])
                self._results = batch_result["result"]
        finally:
            self._config.logger.debug("finish call_list_fast")

    def call(self) -> JSONDict:
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
) -> JSONDict:
    """
    Retrieve a large classic list result using ID-window pagination.

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
        params: Base method parameters sent to Bitrix.
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
