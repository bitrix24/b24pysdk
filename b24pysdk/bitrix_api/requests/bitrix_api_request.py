from typing import TYPE_CHECKING, Optional

from ...utils.types import B24APIResult, JSONDict
from ..responses import BitrixAPIResponse
from .abstract_bitrix_api_request import AbstractBitrixAPIRequest
from .bitrix_api_list_request import BitrixAPIListFastRequest, BitrixAPIListRequest

if TYPE_CHECKING:
    from ..responses import BitrixAPITimeResponse


class BitrixAPIRequest(AbstractBitrixAPIRequest[BitrixAPIResponse]):
    """"""

    @property
    def result(self) -> B24APIResult:
        """"""
        return self.response.result

    @property
    def time(self) -> "BitrixAPITimeResponse":
        """"""
        return self.response.time

    @staticmethod
    def _convert_response(response: JSONDict) -> BitrixAPIResponse:
        """"""
        return BitrixAPIResponse.from_dict(response)

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
