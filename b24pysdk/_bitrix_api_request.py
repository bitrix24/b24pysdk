from typing import Optional, Text


from ._bitrix_api_response import BitrixAPIResponse, BitrixResponseTime
from .bitrix_api import BitrixToken
from .utils.types import B24APIResult, JSONDict


class BitrixAPIRequest:
    """"""

    __slots__ = ("_bitrix_token", "_api_method", "_params", "_response", "_timeout")

    _bitrix_token: BitrixToken
    _api_method: Text
    _params: Optional[JSONDict]
    _timeout: Optional[int]
    _response: Optional[BitrixAPIResponse]

    def __init__(
            self,
            *,
            bitrix_token: BitrixToken,
            api_method: Text,
            params: Optional[JSONDict] = None,
            timeout: Optional[int] = None,
    ):
        self._bitrix_token = bitrix_token
        self._api_method = api_method
        self._params = params
        self._timeout = timeout
        self._response = None

    def __str__(self):
        param_string = ", ".join([f"{key}={value}" for key, value in self._params.items()])
        return f"<{self.__class__.__name__} {self._api_method}({param_string})>"

    __repr__ = __str__

    @property
    def api_method(self) -> Text:
        return self._api_method

    @property
    def params(self) -> Optional[JSONDict]:
        return self._params

    @property
    def timeout(self) -> Optional[int]:
        return self._timeout

    @property
    def response(self) -> BitrixAPIResponse:
        return self._response or self.execute()

    @property
    def result(self) -> B24APIResult:
        return self.response.result

    @property
    def time(self) -> BitrixResponseTime:
        return self.response.time

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_api_method(
            api_method=self._api_method,
            params=self._params,
            timeout=self._timeout,
        )

    def execute(self) -> BitrixAPIResponse:
        """"""
        self._response = BitrixAPIResponse.from_dict(self._call())
        return self._response
