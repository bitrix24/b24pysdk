from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Generic, Iterable, TypeVar

from ..._constants import PYTHON_VERSION
from ...utils.types import JSONDict, JSONDictGenerator, JSONList
from .abstract_bitrix_response import AbstractBitrixResponse

if TYPE_CHECKING:
    from .bitrix_time_response import BitrixTimeResponse

__all__ = [
    "AbstractBitrixAPIListResponse",
    "BitrixAPIListFastResponse",
    "BitrixAPIListResponse",
]

_BALRST = TypeVar("_BALRST", bound=Iterable[JSONDict])

_DATACLASS_KWARGS = {"repr": False, "eq": False, "frozen": True}

if PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True


@dataclass(**_DATACLASS_KWARGS)
class AbstractBitrixAPIListResponse(AbstractBitrixResponse[_BALRST], ABC, Generic[_BALRST]):
    """
    Base class for Bitrix24 list responses.

    Represents responses whose ``result`` field is an iterable collection of
    JSON objects.
    """


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIListResponse(AbstractBitrixAPIListResponse[JSONList]):
    """
    Standard Bitrix24 list response.

    Stores a fully loaded list result returned by standard list pagination.
    """

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result=<list: {len(self.result)}>, "
            f"time={self.time})"
        )

    @classmethod
    def from_dict(cls, json_response: JSONDict, /) -> "BitrixAPIListResponse":
        """
        Create a BitrixAPIListResponse instance from raw JSON response.

        Args:
            json_response: Raw JSON response returned by ``call_list``.

        Returns:
            Parsed list response with fully loaded result items.
        """
        return cls(
            result=json_response["result"],
            time=cls._convert_time(json_response["time"]),
        )


@dataclass(**_DATACLASS_KWARGS)
class BitrixAPIListFastResponse(AbstractBitrixAPIListResponse[JSONDictGenerator]):
    """
    Fast Bitrix24 list response.

    Stores a lazy one-time generator returned by fast ID-window pagination.
    Items are fetched progressively while the generator is consumed.

    The ``time`` metadata is backed by a mutable raw timing dictionary and
    reflects the current accumulated timing values. Final timing values are
    available only after the result generator has been fully consumed.
    """

    time: InitVar[JSONDict]
    _time: JSONDict = field(init=False)

    def __post_init__(self, time: JSONDict):
        """
        Store mutable raw timing metadata.

        Args:
            time: Mutable timing dictionary updated during generator iteration.
        """
        object.__setattr__(self, "_time", time)

    @property
    def time(self) -> "BitrixTimeResponse":
        """
        Return current accumulated timing metadata.

        The returned value is recalculated from the mutable raw timing
        dictionary each time this property is accessed.
        """
        return self._convert_time(self._time)

    @classmethod
    def from_dict(cls, json_response: JSONDict, /) -> "BitrixAPIListFastResponse":
        """
        Create a BitrixAPIListFastResponse instance from raw JSON response.

        Args:
            json_response: Raw JSON response returned by ``call_list_fast``.

        Returns:
            Parsed fast list response with lazy one-time result generator.
        """
        return cls(
            result=json_response["result"],
            time=json_response["time"],
        )

    def to_dict(self) -> JSONDict:
        """
        Convert fast list response to dictionary.

        Warning:
            This method consumes the one-time ``result`` generator by converting
            it to a list. After calling this method, the generator should be
            treated as exhausted.

        Returns:
            Dictionary representation of the response.
        """
        return {
            "result": list(self.result),
            "time": self.time.to_dict(),
        }
