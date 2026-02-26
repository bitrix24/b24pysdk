from typing import Optional

from ...utils.types import JSONDict
from ..responses import BitrixAPIResponse
from .bitrix_api_base_request import BitrixAPIBaseRequest
from .bitrix_api_list_request import BitrixAPIListFastRequest, BitrixAPIListRequest

__all__ = [
    "BitrixAPIRequest",
]


class BitrixAPIRequest(BitrixAPIBaseRequest[BitrixAPIResponse]):
    """"""

    __slots__ = ()

    @staticmethod
    def _convert_response(json_response: JSONDict) -> BitrixAPIResponse:
        """"""
        return BitrixAPIResponse.from_dict(json_response)

    def as_list(
            self,
            limit: Optional[int] = None,
    ) -> BitrixAPIListRequest:
        """"""
        return BitrixAPIListRequest(
            bitrix_api_request=self,
            limit=limit,
            **self._kwargs,
        )

    def as_list_fast(
            self,
            descending: bool = False,
            limit: Optional[int] = None,
    ) -> BitrixAPIListFastRequest:
        """"""
        return BitrixAPIListFastRequest(
            bitrix_api_request=self,
            descending=descending,
            limit=limit,
            **self._kwargs,
        )
