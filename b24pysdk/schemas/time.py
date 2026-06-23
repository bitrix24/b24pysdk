from typing import Text, TypedDict

__all__ = [
    "TimeData",
]


class _TimeOptionalData(TypedDict, total=False):
    operating_reset_at: float
    operating: float


class TimeData(_TimeOptionalData):
    start: float
    finish: float
    duration: float
    processing: float
    date_start: Text
    date_finish: Text
