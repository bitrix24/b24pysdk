from abc import ABC
from typing import TYPE_CHECKING, Generic, TypeVar

from ..responses import AbstractBitrixResponse
from .abstract_bitrix_api_request import AbstractBitrixAPIRequest

if TYPE_CHECKING:
    from ..responses import BitrixTimeResponse

__all__ = [
    "BitrixAPIBaseRequest",
]

_BARPT = TypeVar("_BARPT", bound=AbstractBitrixResponse)


class BitrixAPIBaseRequest(AbstractBitrixAPIRequest[_BARPT], ABC, Generic[_BARPT]):
    """
    Base class for Bitrix24 API request objects with standard response shape.

    Extends ``AbstractBitrixAPIRequest`` for responses that expose common
    ``result`` and ``time`` fields.
    """

    __slots__ = ()

    @property
    def result(self):
        """
        Return result data from the response.

        Accessing this property may execute the request lazily on first access.
        """
        return self.response.result

    @property
    def time(self) -> "BitrixTimeResponse":
        """
        Return Bitrix24 timing metadata from the response.

        Accessing this property may execute the request lazily on first access.
        """
        return self.response.time
