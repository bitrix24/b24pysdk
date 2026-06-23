from dataclasses import dataclass
from typing import Generic, Optional

from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.type_vars import BAResultT
from ...utils.types import JSONDict
from .abstract_bitrix_response import AbstractBitrixResponse

__all__ = [
    "BitrixAPIResponse",
]


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIResponse(AbstractBitrixResponse[BAResultT], Generic[BAResultT]):
    """
    Standard Bitrix24 API response.

    Represents a regular REST API response containing ``result`` and ``time``,
    with optional pagination metadata returned by list-like methods.
    """

    next: Optional[int]
    total: Optional[int]

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result={self.result}, "
            f"time={self.time}, "
            f"next={self.next}, "
            f"total={self.total})"
        )

    @classmethod
    def from_dict(cls, json_response: JSONDict, /) -> "BitrixAPIResponse[BAResultT]":
        """
        Create a BitrixAPIResponse instance from raw JSON response.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed standard API response.
        """
        return cls(
            result=json_response["result"],
            time=cls._convert_time(json_response["time"]),
            next=json_response.get("next"),
            total=json_response.get("total"),
        )
