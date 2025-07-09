from typing import Optional, Text, Tuple

from ...utils.types import B24APIResult, JSONDict, Timeout
from ..bitrix_token import AbstractBitrixToken
from .bitrix_api_response import BitrixAPIResponse
from .bitrix_api_response_time import BitrixAPIResponseTime


class BitrixAPIRequest:
    """"""

    __slots__ = ("_bitrix_token", "_api_method", "_params", "_response", "_timeout")

    _bitrix_token: AbstractBitrixToken
    _api_method: Text
    _params: Optional[JSONDict]
    _timeout: Timeout
    _response: Optional[BitrixAPIResponse]

    def __init__(
            self,
            *,
            bitrix_token: AbstractBitrixToken,
            api_method: Text,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ):
        self._bitrix_token = bitrix_token
        self._api_method = api_method
        self._params = params
        self._timeout = timeout
        self._response = None

    def __str__(self):
        if isinstance(self._params, dict):
            param_string = ", ".join([f"{key}={value}" for key, value in self._params.items()])
        else:
            param_string = ""

        return f"<{self.__class__.__name__} {self._api_method}({param_string})>"

    __repr__ = __str__

    @property
    def api_method(self) -> Text:
        return self._api_method

    @property
    def params(self) -> Optional[JSONDict]:
        return self._params

    @property
    def timeout(self) -> Timeout:
        return self._timeout

    @property
    def response(self) -> BitrixAPIResponse:
        return self._response or self.execute()

    @property
    def result(self) -> B24APIResult:
        return self.response.result

    @property
    def time(self) -> BitrixAPIResponseTime:
        return self.response.time

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_method(
            api_method=self._api_method,
            params=self._params,
            timeout=self._timeout,
        )

    def execute(self) -> BitrixAPIResponse:
        """"""
        self._response = BitrixAPIResponse.from_dict(self._call())
        return self._response

    def as_tuple(self) -> Tuple[Text, Optional[JSONDict]]:
        """"""
        return self._api_method, self._params
