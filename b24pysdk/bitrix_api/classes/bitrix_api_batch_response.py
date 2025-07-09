from dataclasses import dataclass
from typing import Dict, List, Text, Union

from ..._constants import PYTHON_VERSION
from ...utils.types import B24APIResult, JSONDict, JSONList
from .bitrix_api_response import BitrixAPIResponse
from .bitrix_api_response_time import BitrixAPIResponseTime

DATACLASS_KWARGS = {"eq": False, "order": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    DATACLASS_KWARGS["slots"] = True


@dataclass(**DATACLASS_KWARGS)
class B24APIBatchResult:
    """"""

    result: Union[Dict[Text, B24APIResult], List[B24APIResult]]
    result_error: Union[JSONDict, JSONList]
    result_total: Union[Dict[Text, int], List[int]]
    result_next: Union[Dict[Text, int], List[int]]
    result_time: Union[Dict[Text, BitrixAPIResponseTime], List[BitrixAPIResponseTime]]

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "B24APIBatchResult":
        json_result_time = json_response["result_time"]

        if isinstance(json_result_time, dict):
            result_time = dict()

            for key, time_value in json_result_time.items():
                result_time[key] = BitrixAPIResponseTime.from_dict(time_value)

        else:
            result_time = list()

            for time_value in json_result_time:
                result_time.append(BitrixAPIResponseTime.from_dict(time_value))

        return cls(
            result=json_response["result"],
            result_error=json_response["result_error"],
            result_total=json_response["result_total"],
            result_next=json_response["result_next"],
            result_time=result_time,
        )

    def to_dict(self) -> JSONDict:
        return {
            "result": self.result,
            "result_error": self.result_error,
            "result_total": self.result_total,
            "result_next": self.result_next,
            "result_time": self.result_time,
        }


@dataclass(**DATACLASS_KWARGS)
class BitrixAPIBatchResponse(BitrixAPIResponse):
    """"""

    result: B24APIBatchResult

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIBatchResponse":
        return cls(
            result=B24APIBatchResult.from_dict(json_response["result"]),
            time=BitrixAPIResponseTime.from_dict(json_response["time"]),
        )

    def to_dict(self) -> JSONDict:
        return {
            "result": self.result,
            "time": self.time,
        }
