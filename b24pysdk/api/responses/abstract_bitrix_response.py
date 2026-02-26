from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Generic, TypeVar

from ..._constants import PYTHON_VERSION
from ...utils.types import JSONDict
from .bitrix_time_response import BitrixTimeResponse

__all__ = [
    "AbstractBitrixResponse",
]

_BARST = TypeVar("_BARST")

_DATACLASS_KWARGS = {"repr": False, "eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class AbstractBitrixResponse(ABC, Generic[_BARST]):
    """"""

    result: _BARST
    time: "BitrixTimeResponse"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result={self.result}, "
            f"time={self.time})"
        )

    @staticmethod
    def _convert_time(json_response: JSONDict) -> BitrixTimeResponse:
        """"""
        return BitrixTimeResponse.from_dict(json_response)

    @classmethod
    @abstractmethod
    def from_dict(cls, json_response: JSONDict) -> "AbstractBitrixResponse":
        """"""
        raise NotImplementedError

    def to_dict(self) -> JSONDict:
        return asdict(self)
