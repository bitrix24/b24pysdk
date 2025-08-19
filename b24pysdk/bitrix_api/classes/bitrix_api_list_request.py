from typing import Optional

from ...utils.types import JSONDict, JSONList
from ..bitrix_token import AbstractBitrixToken
from .bitrix_api_request import BitrixAPIRequest
from .bitrix_api_response import BitrixAPIListResponse


class BitrixAPIListRequest(BitrixAPIRequest):
    """"""

    __slots__ = ("_limit",)

    _response: Optional[BitrixAPIListResponse]
    _limit: Optional[int]

    def __init__(
            self,
            *,
            bitrix_token: AbstractBitrixToken,
            bitrix_api_request: BitrixAPIRequest,
            limit: Optional[int] = None,
    ):
        super().__init__(
            bitrix_token=bitrix_token,
            api_method=bitrix_api_request.api_method,
            params=bitrix_api_request.params,
            timeout=bitrix_api_request.timeout,
        )
        self._limit = limit

    @property
    def response(self) -> BitrixAPIListResponse:
        return self._response or self.call()

    @property
    def result(self) -> JSONList:
        return self.response.result

    @property
    def limit(self) -> int:
        """"""
        return self._limit

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_list(
            api_method=self._api_method,
            params=self._params,
            limit=self._limit,
            timeout=self._timeout,
        )

    def call(self) -> BitrixAPIListResponse:
        """"""
        self._response = BitrixAPIListResponse.from_dict(self._call())
        return self._response
