from dataclasses import dataclass, field
from typing import Generator, Literal

from ...._constants import PYTHON_VERSION
from ....utils.types import JSONDict, JSONList
from .bitrix_api_response import BitrixAPIResponse
from .bitrix_api_time_response import BitrixAPITimeResponse

_DATACLASS_KWARGS = {"repr": False, "eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIListResponse(BitrixAPIResponse):
    """"""

    result: JSONList
    next: Literal[None] = field(init=False, default=None)
    total: Literal[None] = field(init=False, default=None)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result=<list: {len(self.result)}>, "
            f"time={self.time})"
        )

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIListResponse":
        return cls(
            result=json_response["result"],
            _time=BitrixAPITimeResponse.from_dict(json_response["time"]),
        )


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIListFastResponse(BitrixAPIListResponse):
    """"""

    result: Generator[JSONDict, None, None]
    _time: JSONDict

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result={self.result}, "
            f"time={self.time})"
        )

    @property
    def time(self) -> BitrixAPITimeResponse:
        return BitrixAPITimeResponse.from_dict(self._time)

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIListFastResponse":
        return cls(
            result=json_response["result"],
            _time=json_response["time"],
        )
