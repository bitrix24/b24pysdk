from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..._config import Config
from ...schemas.api import TimeResponseData
from ...utils.converters import datetime_from_bitrix, datetime_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs

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
    def from_dict(cls, json_response: TimeResponseData, /) -> "BitrixTimeResponse":
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
            date_start=datetime_from_bitrix(json_response["date_start"], is_required=True),
            date_finish=datetime_from_bitrix(json_response["date_finish"], is_required=True),
            operating_reset_at=json_response.get("operating_reset_at") and datetime.fromtimestamp(json_response["operating_reset_at"], tz=Config().tz),
            operating=json_response.get("operating"),
        )

    def to_dict(self) -> TimeResponseData:
        """
        Convert timing metadata to raw Bitrix24 time payload shape.

        Returns:
            Dictionary representation of the timing metadata.
        """

        time_response_data: TimeResponseData = {
            "start": self.start,
            "finish": self.finish,
            "duration": self.duration,
            "processing": self.processing,
            "date_start": datetime_to_bitrix(self.date_start, is_required=True),
            "date_finish": datetime_to_bitrix(self.date_finish, is_required=True),
        }

        if self.operating_reset_at is not None:
            time_response_data["operating_reset_at"] = self.operating_reset_at.timestamp()

        if self.operating is not None:
            time_response_data["operating"] = self.operating

        return time_response_data
