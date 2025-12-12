from typing import Optional

from ...utils.types import JSONDict, JSONDictGenerator, JSONList
from ..responses import BitrixAPIListFastResponse, BitrixAPIListResponse
from .bitrix_api_request import BitrixAPIRequest


class BitrixAPIListRequest(BitrixAPIRequest):
    """"""

    __slots__ = ("_limit",)

    _response: Optional[BitrixAPIListResponse]
    _limit: Optional[int]

    def __init__(
            self,
            *,
            bitrix_api_request: BitrixAPIRequest,
            limit: Optional[int] = None,
            **kwargs,
    ):
        super().__init__(
            bitrix_token=bitrix_api_request.bitrix_token,
            api_method=bitrix_api_request.api_method,
            params=bitrix_api_request.params,
            timeout=bitrix_api_request.timeout,
            **kwargs,
        )
        self._limit = limit

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"api_method='{self._api_method}', "
            f"params={self._params}, "
            f"limit={self._limit}, "
            f"timeout={self._timeout})"
        )

    @property
    def limit(self) -> int:
        """"""
        return self._limit

    @property
    def response(self) -> BitrixAPIListResponse:
        """"""
        return self._response or self.call()

    @property
    def result(self) -> JSONList:
        """"""
        return self.response.result

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_list(
            api_method=self._api_method,
            params=self._params,
            limit=self._limit,
            timeout=self._timeout,
            **self._kwargs,
        )

    def call(self) -> BitrixAPIListResponse:
        """"""
        self._response = BitrixAPIListResponse.from_dict(self._call())
        return self._response


class BitrixAPIListFastRequest(BitrixAPIListRequest):
    """"""

    __slots__ = ("_descending",)

    _response: Optional[BitrixAPIListFastResponse]
    _descending: bool

    def __init__(
            self,
            *,
            bitrix_api_request: BitrixAPIRequest,
            descending: bool = False,
            limit: Optional[int] = None,
            **kwargs,
    ):
        super().__init__(
            bitrix_api_request=bitrix_api_request,
            limit=limit,
            **kwargs,
        )
        self._descending = descending

    @property
    def descending(self) -> bool:
        """"""
        return self._descending

    @property
    def response(self) -> BitrixAPIListFastResponse:
        """"""
        return self._response or self.call()

    @property
    def result(self) -> JSONDictGenerator:
        """"""
        return self.response.result

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_list_fast(
            api_method=self._api_method,
            params=self._params,
            descending=self._descending,
            limit=self._limit,
            timeout=self._timeout,
            **self._kwargs,
        )

    def call(self) -> BitrixAPIListFastResponse:
        """"""
        self._response = BitrixAPIListFastResponse.from_dict(self._call())
        return self._response
