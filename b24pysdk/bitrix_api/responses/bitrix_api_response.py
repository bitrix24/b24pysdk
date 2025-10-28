from dataclasses import asdict, dataclass
from typing import Dict, Optional

from ..._constants import PYTHON_VERSION as _PV
from ...utils.types import B24APIResult, JSONDict
from .bitrix_api_time_response import BitrixAPITimeResponse

_DATACLASS_KWARGS = {"repr": False, "eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIResponse:
    """"""

    result: B24APIResult
    time: BitrixAPITimeResponse
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
            time=BitrixAPITimeResponse.from_dict(json_response["time"]),
            next=json_response.get("next"),
            total=json_response.get("total"),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
