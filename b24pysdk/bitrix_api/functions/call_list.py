from typing import Final, Iterable, List, Mapping, Optional, Text, Tuple

from ..._constants import MAX_BATCH_SIZE
from ...utils.types import B24BatchRequestData, JSONDict, JSONList, Timeout
from ._base_caller import BaseCaller
from .call_batches import call_batches
from .call_method import call_method


class _ListCaller(BaseCaller):
    """"""

    _ALLOWED_PARAMS_FOR_OPTIMIZATION_BY_ID: Final[Tuple] = ("filter", "select")
    _FILTER_ID_KEYS: Final[Tuple] = ("id", "@id")
    _HALT: Final[bool] = True
    _STEP: Final[int] = MAX_BATCH_SIZE

    __slots__ = ("_limit", "_time")

    _limit: int
    _time: Optional[JSONDict]

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            api_method: Text,
            params: Optional[JSONDict] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
            **kwargs,
    ):
        super().__init__(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=api_method,
            params=params,
            timeout=timeout,
            **kwargs,
        )
        self._limit = limit
        self._time = None

    def _check_filter_by_id_only(self) -> Tuple[Text, Text, List[int]]:
        """
        Checks if method params contain only single filter by list of ids

        Returns:
            key by which filter values can be accessed

            key by which list of ids in filter can be accessed

            list of ids to filter by if params satisfy the condition, otherwise None
        """

        filter_key = ""
        filter_id_key = ""
        filter_ids = []

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

        filter_id_value = self._params[filter_key][filter_id_key]

        if isinstance(filter_id_value, Iterable) and not isinstance(filter_id_value, (str, bytes)):
            filter_ids = list(filter_id_value)

        return filter_key, filter_id_key, filter_ids

    def _generate_filter_id_methods_for_batch(
            self,
            filter_key: Text,
            filter_id_key: Text,
            filter_ids: List[int],
    ) -> List[B24BatchRequestData]:
        """
        Generates list of methods, using call_list() api_method and params, slicing ids from filter parameter in chunks

        Returns:
            list of B24BatchRequestData, ready to be used by call_batches()
        """

        methods: List[B24BatchRequestData] = list()

        for start in range(0, len(filter_ids), self._STEP):
            id_chunk = filter_ids[start:start + self._STEP]
            chunk_params = self._params | {filter_key: {filter_id_key: id_chunk}}
            methods.append((self._api_method, chunk_params))

        return methods

    def _generate_methods_for_batch(
            self,
            next_step: int,
            total: int,
    ) -> List[B24BatchRequestData]:
        """
        Generates list of methods, using call_list() api_method and params, adding pagination parameter
        Args:
            next_step: index from which generation starts
            total: total number of list method's results

        Returns:
            list of B24BatchRequestData, ready to be used by call_batches()
        """

        methods: List[B24BatchRequestData] = list()

        for start in range(next_step, total, self._STEP):
            page_params = self._params | {"start": start}
            methods.append((self._api_method, page_params))

        return methods

    def _fetch_first_response(self) -> JSONDict:
        """"""
        return call_method(
            domain=self._domain,
            auth_token=self._auth_token,
            is_webhook=self._is_webhook,
            api_method=self._api_method,
            params=self._params,
            timeout=self._timeout,
            **self._kwargs,
        )

    def _fetch_batches_response(self, methods: List[B24BatchRequestData]) -> JSONDict:
        """"""
        return call_batches(
            domain=self._domain,
            auth_token=self._auth_token,
            is_webhook=self._is_webhook,
            methods=methods,
            halt=self._HALT,
            timeout=self._timeout,
            **self._kwargs,
        )

    def _unwrap_result(self, result: JSONDict) -> JSONList:
        """"""

        while isinstance(result, dict):
            result = next(iter(result.values()))

        if isinstance(result, list):
            return result
        else:
            raise TypeError(f"API method '{self._api_method}' is not a list method!")

    def _unwrap_batch_result(self, batch_result: JSONDict) -> JSONList:
        """"""

        result_list = list()

        if isinstance(batch_result["result"], dict):
            result_values = batch_result["result"].values()
        else:
            result_values = batch_result["result"]

        for result_value in result_values:
            result_list.extend(self._unwrap_result(result_value))

        return result_list

    def _add_time(self, time: JSONDict):
        """"""

        self._time["finish"] = time["finish"]
        self._time["duration"] += time["duration"]
        self._time["processing"] += time["processing"]
        self._time["date_finish"] = time["date_finish"]

        if self._time.get("operating_reset_at") is not None:
            self._time["operating_reset_at"] = time["operating_reset_at"]

        if self._time.get("operating") is not None:
            self._time["operating"] = time["operating"]

    def call(self) -> JSONDict:
        """"""

        filter_key, filter_id_key, filter_ids = self._check_filter_by_id_only()

        if filter_ids:
            batch_response = self._fetch_batches_response(
                methods=self._generate_filter_id_methods_for_batch(
                    filter_key=filter_key,
                    filter_id_key=filter_id_key,
                    filter_ids=filter_ids,
                ),
            )
            batch_response["result"] = self._unwrap_batch_result(batch_response["result"])[:self._limit]
            return batch_response

        response = self._fetch_first_response()

        result = self._unwrap_result(response["result"])
        self._time = response["time"]

        next_step = response.get("next")

        total = response.get("total") or 0
        total = min(total, self._limit) if self._limit else total

        if next_step:
            batch_response = self._fetch_batches_response(
                methods=self._generate_methods_for_batch(
                    next_step=next_step,
                    total=total,
                ),
            )
            result.extend(self._unwrap_batch_result(batch_response["result"]))
            self._add_time(batch_response["time"])

        return dict(result=result[:total], time=self._time)


def call_list(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        api_method: Text,
        params: Optional[JSONDict] = None,
        limit: Optional[int] = None,
        timeout: Timeout = None,
        **kwargs,
) -> JSONDict:
    """
    Retrieve large number of items using batch API method and accounting for pagination

    Args:
        domain: bitrix portal domain
        auth_token: auth token
        is_webhook: whether the method is being called using webhook token
        api_method: name of the bitrix API method to call, e.g. crm.deal.list
        params: API method parameters
        limit: max number of items to retrieve
        timeout: timeout in seconds

    Returns:
        dictionary containing list of items returned by called API method and information about call time
    """
    return _ListCaller(
        domain=domain,
        auth_token=auth_token,
        is_webhook=is_webhook,
        api_method=api_method,
        params=params,
        limit=limit,
        timeout=timeout,
        **kwargs,
    ).call()
