from abc import ABC
from typing import TYPE_CHECKING, Optional, TypeVar

from ...utils.types import JSONDict, JSONDictGenerator, JSONList
from ..responses import BitrixAPIListFastResponse, BitrixAPIListResponse
from .abstract_bitrix_api_request import AbstractBitrixAPIRequest

if TYPE_CHECKING:
    from ..responses import BitrixAPITimeResponse


_BALRPT = TypeVar("_BALRPT", bound=BitrixAPIListResponse)


class _AbstractBitrixAPIListRequest(AbstractBitrixAPIRequest[_BALRPT], ABC):
    """"""

    __slots__ = ("_limit",)

    _limit: Optional[int]

    def __init__(
            self,
            *,
            bitrix_api_request: AbstractBitrixAPIRequest,
            limit: Optional[int] = None,
            **kwargs,
    ):
        super().__init__(
            bitrix_token=bitrix_api_request._bitrix_token,
            api_method=bitrix_api_request._api_method,
            params=bitrix_api_request._params,
            **bitrix_api_request._kwargs | kwargs,
        )
        self._limit = limit

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"api_method='{self._api_method}', "
            f"params={self._params}, "
            f"limit={self._limit})"
        )

    @property
    def time(self) -> "BitrixAPITimeResponse":
        """"""
        return self.response.time


class BitrixAPIListRequest(_AbstractBitrixAPIListRequest[BitrixAPIListResponse]):
    """"""

    __slots__ = ()

    @property
    def result(self) -> JSONList:
        """"""
        return self.response.result

    @staticmethod
    def _convert_response(response: JSONDict) -> BitrixAPIListResponse:
        """"""
        return BitrixAPIListResponse.from_dict(response)

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_list(
            api_method=self._api_method,
            params=self._params,
            limit=self._limit,
            **self._kwargs,
        )


class BitrixAPIListFastRequest(_AbstractBitrixAPIListRequest[BitrixAPIListFastResponse]):
    """"""

    __slots__ = ("_descending",)

    _descending: bool

    def __init__(
            self,
            *,
            bitrix_api_request: AbstractBitrixAPIRequest,
            descending: bool = False,
            limit: Optional[int] = None,
            **kwargs,
    ):
        super().__init__(
            bitrix_api_request=bitrix_api_request,
            limit=limit,
            **bitrix_api_request._kwargs | kwargs,
        )
        self._descending = descending

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"api_method='{self._api_method}', "
            f"params={self._params}, "
            f"descending={self._descending}), "
            f"limit={self._limit})"
        )

    @property
    def result(self) -> JSONDictGenerator:
        """"""
        return self.response.result

    @staticmethod
    def _convert_response(response: JSONDict) -> BitrixAPIListFastResponse:
        """"""
        return BitrixAPIListFastResponse.from_dict(response)

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_list_fast(
            api_method=self._api_method,
            params=self._params,
            descending=self._descending,
            limit=self._limit,
            **self._kwargs,
        )
