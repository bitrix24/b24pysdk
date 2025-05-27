from datetime import datetime
from typing import Optional

from .utils.types import B24APIResult, JSONDict


class BitrixResponseTime:
    """"""

    __slots__ = ("start", "finish", "duration", "processing", "date_start", "date_finish", "operating")

    start: float
    finish: float
    duration: float
    processing: float
    date_start: datetime
    date_finish: datetime
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
            operating: Optional[float],
    ):
        self.start = start
        self.finish = finish
        self.duration = duration
        self.processing = processing
        self.date_start = date_start
        self.date_finish = date_finish
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
            "operating": self.operating,
        }


class BitrixAPIResponse:
    """"""

    __slots__ = ("_result", "_time", "_total", "_next")

    _result: B24APIResult
    _time: BitrixResponseTime
    _total: Optional[int]
    _next: Optional[int]

    def __init__(
            self,
            *,
            result: B24APIResult,
            time: BitrixResponseTime,
            total: Optional[int] = None,
            next: Optional[int] = None,
    ):
        self._result = result
        self._time = time
        self._total = total
        self._next = next

    def __str__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

    __repr__ = __str__

    @property
    def result(self) -> B24APIResult:
        return self._result

    @property
    def time(self) -> BitrixResponseTime:
        return self._time

    @property
    def total(self) -> Optional[int]:
        return self._total

    @property
    def next(self) -> Optional[int]:
        return self._next

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
            "result": self._result,
            "time": self._time,
            "total": self._total,
            "next": self._next,
        }
