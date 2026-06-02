from ...utils.types import JSONDict
from .abstract_bitrix_api_request import AbstractBitrixAPIRequest

__all__ = [
    "BitrixAPIRawRequest",
]


class BitrixAPIRawRequest(AbstractBitrixAPIRequest[JSONDict]):
    """
    Lazy request object that returns the raw Bitrix24 JSON response.

    Unlike typed request classes, this class does not wrap or transform the
    response into a response model.
    """

    __slots__ = ()

    @staticmethod
    def _convert_response(json_response: JSONDict) -> JSONDict:
        """
        Return raw JSON response without conversion.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            The same JSON response object.
        """
        return json_response
