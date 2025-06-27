from datetime import datetime
from typing import Optional

from .utils.types import B24APIResult, JSONDict


class BitrixResponseTime:
    """"""

    __slots__ = (
        "start",
        "finish",
        "duration",
        "processing",
        "date_start",
        "date_finish",
        "operating_reset_at",
        "operating",
    )

    start: float
    finish: float
    duration: float
    processing: float
    date_start: datetime
    date_finish: datetime
    operating_reset_at: Optional[datetime]
    operating: Optional[float]

    def __init__(
            self,
            *,
            start: float,
            finish: float,
            duration: float,
            processing: float,
            date_start: datetime,
            date_finish: datetime,
            operating_reset_at: Optional[datetime] = None,
            operating: Optional[float] = None,
    ):
        self.start = start
        self.finish = finish
        self.duration = duration
        self.processing = processing
        self.date_start = date_start
        self.date_finish = date_finish
        self.operating_reset_at = operating_reset_at
        self.operating = operating

    def __str__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

    __repr__ = __str__

    @classmethod
    def from_dict(cls, response_time: JSONDict) -> "BitrixResponseTime":
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


class BitrixAPIResponse:
    """"""

    __slots__ = ("result", "time", "total", "next")

    result: B24APIResult
    time: BitrixResponseTime
    total: Optional[int]
    next: Optional[int]

    def __init__(
            self,
            *,
            result: B24APIResult,
            time: BitrixResponseTime,
            total: Optional[int] = None,
            next: Optional[int] = None,
    ):
        self.result = result
        self.time = time
        self.total = total
        self.next = next

    def __str__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

    __repr__ = __str__

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIResponse":
        return cls(
            result=json_response["result"],
            time=BitrixResponseTime.from_dict(json_response["time"]),
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
