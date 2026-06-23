from datetime import datetime
from typing import Optional

from ..._config import Config
from ...schemas.time import TimeData

__all__ = [
    "get_empty_time",
]


def get_empty_time(date_time: Optional[datetime] = None) -> TimeData:
    """Build synthetic zero-duration timing metadata for responses without API calls."""

    if date_time is None:
        date_time = Config().get_local_datetime()

    timestamp = date_time.timestamp()
    iso_date_time = date_time.isoformat(timespec="seconds")

    return {
        "start": timestamp,
        "finish": timestamp,
        "duration": 0,
        "processing": 0,
        "date_start": iso_date_time,
        "date_finish": iso_date_time,
    }
