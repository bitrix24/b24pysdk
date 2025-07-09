from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..._constants import PYTHON_VERSION
from ...utils.types import JSONDict

DATACLASS_KWARGS = {"eq": False, "order": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    DATACLASS_KWARGS["slots"] = True


@dataclass(**DATACLASS_KWARGS)
class BitrixAPIResponseTime:
    """"""

    start: float
    finish: float
    duration: float
    processing: float
    date_start: datetime
    date_finish: datetime
    operating_reset_at: Optional[datetime] = None
    operating: Optional[float] = None

    def __str__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

    @classmethod
    def from_dict(cls, response_time: JSONDict) -> "BitrixAPIResponseTime":
        return cls(
            start=response_time["start"],
            finish=response_time["finish"],
            duration=response_time["duration"],
            processing=response_time["processing"],
            date_start=datetime.fromisoformat(response_time["date_start"]),
            date_finish=datetime.fromisoformat(response_time["date_finish"]),
            operating_reset_at=response_time.get("operating_reset_at") and datetime.fromtimestamp(response_time["operating_reset_at"]),
            operating=response_time.get("operating"),
        )

    def to_dict(self) -> JSONDict:
        return {
            "start": self.start,
            "finish": self.finish,
            "duration": self.duration,
            "processing": self.processing,
            "date_start": self.date_start,
            "date_finish": self.date_finish,
            "operating_reset_at": self.operating_reset_at,
            "operating": self.operating,
        }
