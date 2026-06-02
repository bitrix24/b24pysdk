from dataclasses import dataclass
from typing import Optional

from ..._constants import PYTHON_VERSION
from ...utils.types import B24APIResult, JSONDict
from .abstract_bitrix_response import AbstractBitrixResponse

__all__ = [
    "BitrixAPIResponse",
]

_DATACLASS_KWARGS = {"repr": False, "eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIResponse(AbstractBitrixResponse[B24APIResult]):
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
    def from_dict(cls, json_response: JSONDict, /) -> "BitrixAPIResponse":
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
