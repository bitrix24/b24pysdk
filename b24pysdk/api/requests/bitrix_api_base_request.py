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
    """"""

    __slots__ = ()

    @property
    def result(self):
        """"""
        return self.response.result

    @property
    def time(self) -> "BitrixTimeResponse":
        """"""
        return self.response.time
