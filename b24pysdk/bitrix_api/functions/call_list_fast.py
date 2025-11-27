from datetime import datetime
from typing import TYPE_CHECKING, Callable, Dict, Final, Generator, Iterable, Literal, Optional, Text, Tuple, Union

from ..._constants import MAX_BATCH_SIZE
from ...utils.types import B24BatchMethodTuple, JSONDict, JSONList, Timeout
from ..protocols import BitrixTokenProtocol
from ._base_caller import BaseCaller
from .call_batch import call_batch
from .call_method import call_method

if TYPE_CHECKING:
    from ..credentials import AbstractBitrixToken


class _ListFastCaller(BaseCaller):
    """"""

    _DEFAULT_ID_FIELD: Final[Text] = "ID"
    _DEFAULT_ORDER_PATTERN: Final[Callable[[Text, Text], JSONDict]] = staticmethod(lambda id_field, sorting: {"order": {id_field: sorting}})
    _HALT: Final[bool] = True
    _MAX_BATCH_SIZE: Final[int] = MAX_BATCH_SIZE
    _START: Final[int] = -1

    _REQUEST_ID_FIELDS: Final[Dict] = {
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
    _time: JSONDict
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
            timeout: Timeout = None,
            bitrix_token: Optional[Union["AbstractBitrixToken", BitrixTokenProtocol]] = None,
            **kwargs,
    ):
        super().__init__(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=api_method,
            params=params,
            timeout=timeout,
            bitrix_token=bitrix_token,
            **kwargs,
        )
        self._descending = descending
        self._limit = limit
        self._now_datetime = datetime.now(tz=self._config.tzinfo)
        self._time = dict(
            start=self._timesampt,
            finish=self._timesampt,
            duration=0,
            processing=0,
            date_start=self._now_datetime.isoformat(timespec="seconds"),
            date_finish=self._now_datetime.isoformat(timespec="seconds"),
        )
        self._counter = 0
        self._last_id = 0
        self._request_id_field = self._get_initial_request_id_field()
        self._response_id_field = None
        self._wrapper = None
        self._order_pattern = self._get_order_pattern()
        self._results = None

    def _get_initial_request_id_field(self) -> Optional[Text]:
        """"""

        api_method = self._api_method
        request_id_field = self._REQUEST_ID_FIELDS.get(api_method)

        while not (api_method.find(".") == -1 or request_id_field):
            api_method, _ = api_method.rsplit(".", maxsplit=1)
            request_id_field = self._REQUEST_ID_FIELDS.get(api_method)

        return request_id_field

    def _get_order_pattern(self) -> Callable[[Text, Text], JSONDict]:
        """"""

        api_method = self._api_method
        order_pattern = self._ORDER_PATTERNS.get(api_method)

        while not (api_method.find(".") == -1 or order_pattern):
            api_method, _ = api_method.rsplit(".", maxsplit=1)
            order_pattern = self._ORDER_PATTERNS.get(api_method)

        return order_pattern or self._DEFAULT_ORDER_PATTERN

    @property
    def _cmp(self) -> Literal[">", "<"]:
        """"""
        return (">", "<")[self._descending]

    @property
    def _dynamic_request_id_field(self) -> Text:
        """"""
        return self._request_id_field or self._response_id_field or self._DEFAULT_ID_FIELD

    @property
    def _prop(self) -> Text:
        """"""
        return f"{self._cmp}{self._dynamic_request_id_field}"

    @property
    def _sorting(self) -> Literal["ASC", "DESC"]:
        """"""
        return ("ASC", "DESC")[self._descending]

    @property
    def _order_by_id(self) -> JSONDict:
        """"""
        return self._order_pattern(self._dynamic_request_id_field, self._sorting)

    @property
    def _timesampt(self) -> float:
        """"""
        return self._now_datetime.timestamp()

    @staticmethod
    def _force_values(collection: Union[JSONDict, JSONList]) -> Iterable[Union[JSONDict, JSONList]]:
        """"""
        if isinstance(collection, dict):
            return collection.values()
        else:
            return collection

    @property
    def _results_values(self) -> Iterable[Union[JSONDict, JSONList]]:
        """"""
        return self._force_values(self._results)

    def _deep_merge(self, *dicts: Dict) -> Dict:
        """
        Merges nested dictionaries recursively
        """

        result_dict: Dict = dict()

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

    def _add_time(self, time: JSONDict):
        """"""

        self._time["finish"] = time["finish"]
        self._time["duration"] += time["duration"]
        self._time["processing"] += time["processing"]
        self._time["date_finish"] = time["date_finish"]

        if time.get("operating_reset_at") is not None:
            self._time["operating_reset_at"] = time["operating_reset_at"]

        if time.get("operating") is not None:
            self._time["operating"] = self._time.get("operating", 0) + time["operating"]

    def _unwrap_result(self, result: JSONDict) -> Tuple[Optional[Text], JSONList]:
        """"""

        wrapper = None

        while isinstance(result, dict):
            wrapper, result = next(iter(result.items()))

        if isinstance(result, list):
            return wrapper, result
        else:
            raise TypeError(f"API method '{self._api_method}' is not a list method!")

    def _get_path(self, index: int) -> Text:
        """"""

        path = f"$result[req_{index - 1}]"

        if self._wrapper:
            path = f"{path}[{self._wrapper}]"

        return path

    def _get_filter_by_id(self, index: int) -> JSONDict:
        """
        Generate filter by id
        """

        if index == 0:
            if self._last_id:
                return {"filter": {self._prop: self._last_id}}
            else:
                return {}

        return {"filter": {self._prop: f"{self._get_path(index)}[{self._MAX_BATCH_SIZE - 1}][{self._response_id_field}]"}}

    def _generate_method_params(self, index: int = 0) -> JSONDict:
        """"""
        return self._deep_merge(
            self._params,
            self._order_by_id,
            self._get_filter_by_id(index=index),
            dict(start=self._START),
        )

    def _generate_batch_methods(self) -> Dict[Text, B24BatchMethodTuple]:
        """
        Generates list of methods, using call_list_fast() api_method and params, adding filter by ID

        Returns:
            dict of B24BatchMethodTuple, ready to be used by call_batches()
        """

        methods: Dict[Text, B24BatchMethodTuple] = dict()

        for index in range(self._MAX_BATCH_SIZE):
            method_params = self._generate_method_params(index=index)
            methods[f"req_{index}"] = (self._api_method, method_params)

        return methods

    def _fetch_first_response(self) -> JSONDict:
        """"""
        if self._bitrix_token:
            return self._bitrix_token.call_method(
                api_method=self._api_method,
                params=self._generate_method_params(),
                timeout=self._timeout,
                **self._kwargs,
            )
        else:
            return call_method(
                domain=self._domain,
                auth_token=self._auth_token,
                is_webhook=self._is_webhook,
                api_method=self._api_method,
                params=self._generate_method_params(),
                timeout=self._timeout,
                **self._kwargs,
            )

    def _fetch_next_batch_response(self) -> JSONDict:
        """"""
        return call_batch(
                domain=self._domain,
                auth_token=self._auth_token,
                is_webhook=self._is_webhook,
                methods=self._generate_batch_methods(),
                halt=self._HALT,
                timeout=self._timeout,
                **self._kwargs,
        )

    def _extract_response_id_field(self, result_value: JSONDict) -> Text:
        """"""

        for key in result_value:
            if key.upper() == self._DEFAULT_ID_FIELD:
                return key

        raise ValueError("ID key is not found in Bitrix responses!")

    def _update_last_id(self, new_last_id: int):
        """"""
        if new_last_id != self._last_id:
            self._last_id = new_last_id
        else:
            raise ValueError(
                "Bitrix API returned the same ID sequence: "
                f"last_id={self._last_id}, new_last_id={new_last_id}. "
                "This can lead to an infinite generation loop!",
            )

    def _generate_result(self) -> Generator[JSONDict, None, None]:
        """"""

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

            new_last_id = int(unwrapped_result_values[-1][self._response_id_field])
            self._update_last_id(new_last_id)

            batch_response = self._fetch_next_batch_response()

            self._add_time(batch_response["time"])
            self._results = batch_response["result"]["result"]

    def call(self) -> JSONDict:
        """"""
        return dict(result=self._generate_result(), time=self._time)


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
        bitrix_token: Optional[Union["AbstractBitrixToken", BitrixTokenProtocol]] = None,
        **kwargs,
) -> JSONDict:
    """
    Retrieve large number of items in a performant way using filter by ID and start=-1 parameter to disable the count of items

    Note:
        On small sets of items (2550 entries and less), call_list() has better performance and should be used instead

    Args:
        domain: bitrix portal domain
        auth_token: auth token
        is_webhook: whether the method is being called using webhook token
        api_method: name of the bitrix API method to call, e.g. crm.deal.list
        params: API method parameters
        limit: max number of items to retrieve
        descending: whether items should be retrieved in descending order
        timeout: timeout in seconds
        bitrix_token:

    Returns:
        dictionary containing list of items returned by called API method and information about call time
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
        bitrix_token=bitrix_token,
        **kwargs,
    ).call()
