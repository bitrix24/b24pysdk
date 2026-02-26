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
    """"""

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
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIResponse":
        return cls(
            result=json_response["result"],
            time=cls._convert_time(json_response["time"]),
            next=json_response.get("next"),
            total=json_response.get("total"),
        )
