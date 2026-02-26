from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from ..._config import Config
from ..._constants import PYTHON_VERSION
from ...utils.types import JSONDict

__all__ = [
    "BitrixTimeResponse",
]

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class BitrixTimeResponse:
    """"""

    start: float
    finish: float
    duration: float
    processing: float
    date_start: datetime
    date_finish: datetime
    operating_reset_at: Optional[datetime] = None
    operating: Optional[float] = None

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixTimeResponse":
        return cls(
            start=json_response["start"],
            finish=json_response["finish"],
            duration=json_response["duration"],
            processing=json_response["processing"],
            date_start=datetime.fromisoformat(json_response["date_start"]),
            date_finish=datetime.fromisoformat(json_response["date_finish"]),
            operating_reset_at=json_response.get("operating_reset_at") and datetime.fromtimestamp(json_response["operating_reset_at"], tz=Config().tz),
            operating=json_response.get("operating"),
        )

    def to_dict(self) -> JSONDict:
        return asdict(self)
