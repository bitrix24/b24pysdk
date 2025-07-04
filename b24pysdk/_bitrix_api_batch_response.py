from typing import Dict, List, Union

from ._bitrix_api_response import BitrixResponseTime
from .utils.types import B24APIResult, JSONDict, JSONList


class BitrixAPIBatchResult:
    """"""

    __slots__ = ("result", "result_error", "result_total", "result_next", "result_time")

    result: Union[JSONDict[B24APIResult], JSONList[B24APIResult]]
    result_error: Union[JSONDict, JSONList]
    result_total: Union[Dict[int], List[int]]
    result_next: Union[Dict[int], List[int]]
    result_time: Union[Dict[BitrixResponseTime], List[BitrixResponseTime]]

    def __init__(
            self,
            *,
            result: Union[JSONDict[B24APIResult], JSONList[B24APIResult]],
            result_error: Union[JSONDict, JSONList],
            result_total: Union[Dict[int], List[int]],
            result_next: Union[Dict[int], List[int]],
            result_time: Union[Dict[BitrixResponseTime], List[BitrixResponseTime]],

    ):
        self.result = result
        self.result_error = result_error
        self.result_total = result_total
        self.result_next = result_next
        self.result_time = result_time

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIBatchResult":
        return cls(
            result=json_response["result"],
            result_error=json_response["result_error"],
            result_total=json_response["result_total"],
            result_next=json_response["result_next"],
            result_time=json_response["result_time"],  # TODO
        )

    def to_dict(self) -> JSONDict:
        return {
            "result": self.result,
            "result_error": self.result_error,
            "result_total": self.result_total,
            "result_next": self.result_next,
            "result_time": self.result_time,
        }


class BitrixAPIBatchResponse:
    """"""

    __slots__ = ("_result", "_time")

    _result: BitrixAPIBatchResult
    _time: BitrixResponseTime

    def __init__(
            self,
            *,
            result: BitrixAPIBatchResult,
            time: BitrixResponseTime,

    ):
        self._result = result
        self._time = time

    def __str__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

    __repr__ = __str__

    @property
    def result(self) -> BitrixAPIBatchResult:
        return self._result

    @property
    def time(self) -> BitrixResponseTime:
        return self._time

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIBatchResponse":
        return cls(
            result=json_response["result"],
            time=BitrixResponseTime.from_dict(json_response["time"]),
        )

    def to_dict(self) -> JSONDict:
        return {
            "result": self._result,
            "time": self._time,
        }
