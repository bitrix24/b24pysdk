from typing import Final, Iterable, List, Mapping, Optional, Text, Tuple, Union

from ..._constants import MAX_BATCH_SIZE
from ...constants.version import B24APIVersion
from ...protocols import BitrixTokenProtocol
from ...schemas.api import BatchResponseData, BatchResultData, ListResponseData, ResponseData, TimeResponseData
from ...utils.types import B24APIVersionLiteral, B24RequestTuple, JSONDict, JSONList, Timeout, cast
from ._base_caller import BaseCaller
from ._utils import get_empty_time
from .call_batches import call_batches
from .call_method import call_method

__all__ = [
    "call_list",
]


class _ListCaller(BaseCaller):
    """
    Caller for classic list methods that return ``total``/``next`` pagination.

    The caller fetches the first page with a normal method call, then uses batch
    requests to load remaining pages by ``start`` offsets. It also has a
    shortcut for requests that filter only by a list of IDs: in that case the ID
    list is split into chunks and fetched through batch calls.
    """

    _ALLOWED_PARAMS_FOR_OPTIMIZATION_BY_ID: Final[Tuple[Text, ...]] = ("filter", "select")
    _FILTER_ID_KEYS: Final[Tuple[Text, ...]] = ("id", "@id")
    _HALT: Final[bool] = True
    _STEP: Final[int] = MAX_BATCH_SIZE

    __slots__ = ("_limit", "_time")

    _limit: Optional[int]
    _time: TimeResponseData

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            api_method: Text,
            params: Optional[JSONDict] = None,
            limit: Optional[int] = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            bitrix_token: Optional[BitrixTokenProtocol] = None,
            **kwargs,
    ):
        """
        Initialize a classic list caller.

        Args:
            domain: Bitrix24 portal domain.
            auth_token: OAuth access token or webhook token.
            is_webhook: Whether ``auth_token`` is a webhook token.
            api_method: List-like REST method name.
            params: Method parameters, usually including ``filter`` and
                ``select``.
            limit: Maximum number of items to return, or ``None`` for all
                available items reported by Bitrix.
            prefer_version: Preferred API version. V3 list methods are rejected
                because this caller relies on classic ``start`` pagination.
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
            raise TypeError("Bitrix API v3 methods are not supported by call_list yet.")
        self._limit = limit

    def _check_filter_by_id_only(self) -> Tuple[Text, Text, List[int]]:
        """
        Detect whether the request can be optimized as ID-only filtering.

        The optimization is safe only when method parameters contain no
        meaningful keys except ``filter`` and ``select``, and the filter itself
        contains only ``id`` or ``@id`` with an iterable list of IDs. Such
        requests can be split into independent batch commands by ID chunks
        instead of using ``start`` pagination.

        Returns:
            A tuple containing the actual filter key, the actual ID-filter key,
            and the list of IDs. Empty strings/list mean the optimization is not
            applicable.
        """

        filter_key: Text = ""
        filter_id_key: Text = ""
        filter_ids: List[int] = []

        for key in self._params:
            if key.lower() == "filter":
                filter_key = key

            if key.lower() not in self._ALLOWED_PARAMS_FOR_OPTIMIZATION_BY_ID:
                return filter_key, filter_id_key, filter_ids

        if not (filter_key and isinstance(self._params[filter_key], Mapping)):
            return filter_key, filter_id_key, filter_ids

        for filter_field in self._params[filter_key]:
            if filter_field.lower() in self._FILTER_ID_KEYS:
                filter_id_key = filter_field
            else:
                return filter_key, filter_id_key, filter_ids

        if not filter_id_key:
            return filter_key, filter_id_key, filter_ids

        filter_id_value = self._params[filter_key][filter_id_key]

        if isinstance(filter_id_value, Iterable) and not isinstance(filter_id_value, (str, bytes)):
            filter_ids = list(filter_id_value)

        return filter_key, filter_id_key, filter_ids

    def _generate_filter_id_methods_for_batch(
            self,
            filter_key: Text,
            filter_id_key: Text,
            filter_ids: List[int],
    ) -> List[B24RequestTuple]:
        """
        Generate batch commands for the ID-filter optimization.

        The ID list is split into chunks of ``_STEP`` IDs. Each generated command
        reuses the original method and parameters but replaces the ID filter
        value with the current chunk.

        Returns:
            List of ``(api_method, params)`` tuples ready for ``call_batches``.
        """

        methods: List[B24RequestTuple] = []

        for start in range(0, len(filter_ids), self._STEP):
            id_chunk = filter_ids[start:start + self._STEP]
            chunk_params = self._params | {filter_key: {filter_id_key: id_chunk}}
            methods.append((self._api_method, chunk_params))

        return methods

    def _generate_methods_for_batch(
            self,
            next_step: int,
            total: int,
    ) -> List[B24RequestTuple]:
        """
        Generate batch commands for classic ``start`` pagination.

        Each command reuses the original method and parameters and adds a
        ``start`` offset. Offsets begin from ``next_step`` returned by the first
        Bitrix response and continue up to ``total``.

        Args:
            next_step: First ``start`` offset that still needs to be fetched.
            total: Total number of items to retrieve.

        Returns:
            List of ``(api_method, params)`` tuples ready for ``call_batches``.
        """

        methods: List[B24RequestTuple] = []

        for start in range(next_step, total, self._STEP):
            page_params = self._params | {"start": start}
            methods.append((self._api_method, page_params))

        return methods

    def _fetch_first_response(self) -> ResponseData:
        """
        Fetch the first page using the original method parameters.

        The first response is required because classic Bitrix list methods
        expose ``total`` and ``next`` only in the normal list response.
        """
        if self._bitrix_token:
            response = self._bitrix_token.call_method(
                api_method=self._api_method,
                params=self._params,
                **self._kwargs,
            )
        else:
            response = call_method(
                domain=self._domain,
                auth_token=self._auth_token,
                is_webhook=self._is_webhook,
                api_method=self._api_method,
                params=self._params,
                **self._kwargs,
            )

        return cast(ResponseData, response)

    def _fetch_batches_response(self, methods: List[B24RequestTuple]) -> BatchResponseData:
        """Execute generated pagination or ID-filter requests through batches."""
        return call_batches(
            domain=self._domain,
            auth_token=self._auth_token,
            is_webhook=self._is_webhook,
            methods=methods,
            halt=self._HALT,
            bitrix_token=self._bitrix_token,
            **self._kwargs,
        )

    def _unwrap_result(self, result: Union[JSONDict, JSONList]) -> JSONList:
        """
        Extract the list payload from a Bitrix list response.

        Many Bitrix methods wrap list data under one or more object keys, for
        example ``{"items": [...]}``. This method follows the first value until
        it reaches the actual list.
        """

        while isinstance(result, dict):
            result = next(iter(result.values()))

        if isinstance(result, list):
            return result
        else:
            raise TypeError(f"Bitrix API method {self._api_method!r} is not a list-type method!")

    def _unwrap_batch_result(self, batch_result: BatchResultData) -> JSONList:
        """Flatten list payloads from all command results in a batch response."""

        result_error = batch_result.get("result_error")

        if result_error:
            self._config.logger.warning(
                "batch result contains errors",
                context={
                    "api_method": self._api_method,
                    "result_error": result_error,
                },
            )

        result_list: JSONList = []

        if isinstance(batch_result["result"], dict):
            result_values = batch_result["result"].values()
        else:
            result_values = batch_result["result"]

        for result_value in result_values:
            result_list.extend(self._unwrap_result(result_value))

        return result_list

    def _add_time(self, time: TimeResponseData):
        """Merge timing metadata from an additional batch response into ``_time``."""

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

    def call(self) -> ListResponseData:
        """
        Fetch list items with classic Bitrix pagination and return a normalized response.

        Returns ``{"result": [...], "time": ...}`` regardless of the original
        wrapper key used by the Bitrix method. When possible, remaining pages
        are fetched through batch requests for fewer HTTP round trips.
        """

        self._config.logger.debug(
            "start call_list",
            context={
                "limit": self._limit,
            },
        )

        try:
            if self._limit is not None and self._limit <= 0:
                return {
                    "result": [],
                    "time": get_empty_time(),
                }

            filter_key, filter_id_key, filter_ids = self._check_filter_by_id_only()

            if filter_ids:
                batch_response = self._fetch_batches_response(
                    methods=self._generate_filter_id_methods_for_batch(
                        filter_key=filter_key,
                        filter_id_key=filter_id_key,
                        filter_ids=filter_ids,
                    ),
                )

                result = self._unwrap_batch_result(batch_response["result"])

                if self._limit is not None:
                    del result[self._limit:]

                return {
                    "result": result,
                    "time": batch_response["time"],
                }

            response = self._fetch_first_response()

            result = self._unwrap_result(response["result"])
            self._time = response["time"]

            next_step = response.get("next")
            total = response.get("total")

            if total is None:
                total = len(result)

                message = (
                    f"Bitrix API method {self._api_method!r} did not return a 'total' field. "
                    "The method is likely not a list-type method and you should use call_method instead of call_list."
                )

                self._config.logger.warning(message)

            if self._limit is not None:
                total = min(total, self._limit)

            if next_step and (self._limit is None or self._limit > self._STEP):
                batch_response = self._fetch_batches_response(
                    methods=self._generate_methods_for_batch(
                        next_step=next_step,
                        total=total,
                    ),
                )
                result.extend(self._unwrap_batch_result(batch_response["result"]))
                self._add_time(batch_response["time"])

            del result[total:]

            return {
                "result": result,
                "time": self._time,
            }

        finally:
            self._config.logger.debug("finish call_list")


def call_list(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        api_method: Text,
        params: Optional[JSONDict] = None,
        limit: Optional[int] = None,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> ListResponseData:
    """
    Retrieve items from a classic Bitrix list method using batch pagination.

    The helper is designed for V1/V2 list methods that return classic Bitrix
    pagination fields such as ``total`` and ``next`` and accept ``start`` as the
    page offset. V3 ``/rest/api`` methods are not supported by this helper
    because their pagination contract is different.

    Args:
        domain: Bitrix24 portal domain.
        auth_token: OAuth access token or webhook token.
        is_webhook: Whether ``auth_token`` is a webhook token.
        api_method: List-like REST method name, for example ``crm.deal.list``.
        params: Method parameters sent to Bitrix.
        limit: Maximum number of items to retrieve.
        timeout: Request timeout in seconds.
        prefer_version: Preferred API version to resolve the method against.
        bitrix_token: Optional token wrapper used by nested execution.
        **kwargs: Extra requester options, such as retry configuration.

    Returns:
        Dictionary with flattened ``result`` list and aggregated ``time`` data.
    """
    return _ListCaller(
        domain=domain,
        auth_token=auth_token,
        is_webhook=is_webhook,
        api_method=api_method,
        params=params,
        limit=limit,
        timeout=timeout,
        prefer_version=prefer_version,
        bitrix_token=bitrix_token,
        **kwargs,
    ).call()
