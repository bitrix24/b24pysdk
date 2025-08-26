from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from ..._constants import PYTHON_VERSION
from ...utils.types import JSONDict

_DATACLASS_KWARGS = {"eq": False, "order": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
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

    @classmethod
    def from_dict(cls, response_time: JSONDict) -> "BitrixAPIResponseTime":
        return cls(
            start=response_time["start"],
            finish=response_time["finish"],
            duration=response_time["duration"],
            processing=response_time["processing"],
            date_start=datetime.fromisoformat(response_time["date_start"]),
            date_finish=datetime.fromisoformat(response_time["date_finish"]),
            operating_reset_at=response_time.get("operating_reset_at") and datetime.fromtimestamp(response_time["operating_reset_at"]).astimezone(),
            operating=response_time.get("operating"),
        )

    def to_dict(self) -> JSONDict:
        return asdict(self)
