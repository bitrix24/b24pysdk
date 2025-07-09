from dataclasses import dataclass
from typing import Optional

from ..._constants import PYTHON_VERSION
from ...utils.types import B24APIResult, JSONDict
from .bitrix_api_response_time import BitrixAPIResponseTime

DATACLASS_KWARGS = {"eq": False, "order": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    DATACLASS_KWARGS["slots"] = True


@dataclass(**DATACLASS_KWARGS)
class BitrixAPIResponse:
    """"""

    result: B24APIResult
    time: BitrixAPIResponseTime
    total: Optional[int] = None
    next: Optional[int] = None

    def __str__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIResponse":
        return cls(
            result=json_response["result"],
            time=BitrixAPIResponseTime.from_dict(json_response["time"]),
            total=json_response.get("total"),
            next=json_response.get("next"),
        )

    def to_dict(self) -> JSONDict:
        return {
            "result": self.result,
            "time": self.time,
            "total": self.total,
            "next": self.next,
        }
