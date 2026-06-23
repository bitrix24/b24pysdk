from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from ..._config import Config
from ...schemas.time import TimeData
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import JSONDict

__all__ = [
    "BitrixTimeResponse",
]


@dataclass(**frozen_dataclass_kwargs(eq=False))
class BitrixTimeResponse:
    """
    Timing metadata returned by Bitrix24 API responses.

    Stores request timing, server processing time, and optional operating-limit
    data returned by Bitrix24.
    """

    start: float
    finish: float
    duration: float
    processing: float
    date_start: datetime
    date_finish: datetime
    operating_reset_at: Optional[datetime] = None
    operating: Optional[float] = None

    @classmethod
    def from_dict(cls, json_response: TimeData, /) -> "BitrixTimeResponse":
        """
        Create a BitrixTimeResponse instance from raw timing data.

        Args:
            json_response: Raw ``time`` section from a Bitrix24 response.

        Returns:
            Parsed timing metadata.
        """
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
        """
        Convert timing metadata to dictionary.

        Returns:
            Dictionary representation of the timing metadata.
        """
        return asdict(self)
