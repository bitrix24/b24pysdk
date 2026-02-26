from ...utils.types import JSONDict
from .abstract_bitrix_api_request import AbstractBitrixAPIRequest

__all__ = [
    "BitrixAPIRawRequest",
]


class BitrixAPIRawRequest(AbstractBitrixAPIRequest[JSONDict]):
    """"""

    __slots__ = ()

    @staticmethod
    def _convert_response(json_response: JSONDict) -> JSONDict:
        """"""
        return json_response
