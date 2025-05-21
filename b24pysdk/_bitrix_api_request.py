from typing import Optional, Text, Union


from ._bitrix_api_response import BitrixAPIResponse, BitrixResponseTime
from .bitrix_api import BitrixToken
from .utils.types import JSONDict, JSONList


class BitrixAPIRequest:
    """"""

    __slots__ = ("_bitrix_token", "_api_method", "_params", "_response", "_timeout")

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
        if self._response is None:
            self._response = self._call()
        return self._response

    @property
    def result(self) -> Union[JSONDict, JSONList, bool]:
        return self.response.result

    @property
    def time(self) -> BitrixResponseTime:
        return self.response.time

    def _call(self) -> BitrixAPIResponse:
        json_response = self._bitrix_token.call_api_method(
            api_method=self._api_method,
            params=self._params,
            timeout=self._timeout,
        )
        return BitrixAPIResponse.from_dict(json_response)
