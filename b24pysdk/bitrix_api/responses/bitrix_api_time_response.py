from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, Optional

from ..._config import Config
from ..._constants import PYTHON_VERSION as _PV
from ...utils.types import JSONDict

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _PV >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPITimeResponse:
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
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPITimeResponse":
        return cls(
            start=json_response["start"],
            finish=json_response["finish"],
            duration=json_response["duration"],
            processing=json_response["processing"],
            date_start=datetime.fromisoformat(json_response["date_start"]),
            date_finish=datetime.fromisoformat(json_response["date_finish"]),
            operating_reset_at=json_response.get("operating_reset_at") and datetime.fromtimestamp(json_response["operating_reset_at"], tz=Config().tzinfo),
            operating=json_response.get("operating"),
        )

    def to_dict(self) -> Dict:
        return asdict(self)
