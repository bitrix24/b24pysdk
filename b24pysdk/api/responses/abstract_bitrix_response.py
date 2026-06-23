from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Generic

from ...schemas.time import TimeData
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.type_vars import BAResultT
from ...utils.types import JSONDict
from .bitrix_time_response import BitrixTimeResponse

__all__ = [
    "AbstractBitrixResponse",
]


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class AbstractBitrixResponse(ABC, Generic[BAResultT]):
    """
    Base class for typed Bitrix24 API responses.

    Stores the parsed ``result`` payload together with Bitrix24 timing metadata.
    Concrete subclasses define how raw JSON responses are converted into typed
    response objects.
    """

    result: BAResultT
    time: "BitrixTimeResponse"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result={self.result}, "
            f"time={self.time})"
        )

    @staticmethod
    def _convert_time(json_response: TimeData, /) -> BitrixTimeResponse:
        """
        Convert raw Bitrix24 timing data into ``BitrixTimeResponse``.

        Args:
            json_response: Raw ``time`` section from a Bitrix24 response.

        Returns:
            Parsed timing metadata.
        """
        return BitrixTimeResponse.from_dict(json_response)

    @classmethod
    @abstractmethod
    def from_dict(cls, json_response: JSONDict, /) -> "AbstractBitrixResponse[BAResultT]":
        """
        Create a response object from raw Bitrix24 JSON response.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed response object.
        """
        raise NotImplementedError

    def to_dict(self) -> JSONDict:
        """
        Convert response object to dictionary.

        Returns:
            Dictionary representation of the response.
        """
        return asdict(self)
