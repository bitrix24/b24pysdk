from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Generic, Iterable, TypeVar

from ..._constants import PYTHON_VERSION
from ...utils.types import JSONDict, JSONDictGenerator, JSONList
from .abstract_bitrix_response import AbstractBitrixResponse

if TYPE_CHECKING:
    from .bitrix_time_response import BitrixTimeResponse

__all__ = [
    "AbatractBitrixAPIListResponse",
    "BitrixAPIListFastResponse",
    "BitrixAPIListResponse",
]

_BALRST = TypeVar("_BALRST", bound=Iterable[JSONDict])

_DATACLASS_KWARGS = {"repr": False, "eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class AbatractBitrixAPIListResponse(AbstractBitrixResponse[_BALRST], ABC, Generic[_BALRST]):
    """"""


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIListResponse(AbatractBitrixAPIListResponse[JSONList]):
    """"""

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
            time=cls._convert_time(json_response["time"]),
        )


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIListFastResponse(AbatractBitrixAPIListResponse[JSONDictGenerator]):
    """"""

    time: InitVar[JSONDict]
    _time: JSONDict = field(init=False)

    def __post_init__(self, time: JSONDict):
        object.__setattr__(self, "_time", time)

    @property
    def time(self) -> "BitrixTimeResponse":
        return self._convert_time(self._time)

    @classmethod
    def from_dict(cls, json_response: JSONDict) -> "BitrixAPIListFastResponse":
        return cls(
            result=json_response["result"],
            time=json_response["time"],
        )

    def to_dict(self) -> JSONDict:
        return dict(
            result=list(self.result),
            time=self.time.to_dict(),
        )
