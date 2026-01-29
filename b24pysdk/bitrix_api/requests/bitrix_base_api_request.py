from ...utils.types import JSONDict
from .abstract_bitrix_api_request import AbstractBitrixAPIRequest


class BitrixBaseAPIRequest(AbstractBitrixAPIRequest[JSONDict]):
    """"""

    __slots__ = ()

    @staticmethod
    def _convert_response(response: JSONDict) -> JSONDict:
        """"""
        return response
