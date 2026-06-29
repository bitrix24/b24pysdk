from abc import ABC
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Generic

from ...schemas.api import ListFastResponseData, ListResponseData, TimeResponseData
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.type_vars import BAListResultT
from ...utils.types import JSONGenerator, JSONList
from .abstract_bitrix_response import AbstractBitrixResponse

if TYPE_CHECKING:
    from .bitrix_time_response import BitrixTimeResponse

__all__ = [
    "AbstractBitrixAPIListResponse",
    "BitrixAPIListFastResponse",
    "BitrixAPIListResponse",
]


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class AbstractBitrixAPIListResponse(AbstractBitrixResponse[BAListResultT], ABC, Generic[BAListResultT]):
    """
    Base class for Bitrix24 list responses.

    Represents responses whose ``result`` field is an iterable collection of
    JSON objects.
    """


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
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
    def from_dict(cls, json_response: ListResponseData, /) -> "BitrixAPIListResponse":
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

    def to_dict(self) -> ListResponseData:
        """
        Convert list response to a dictionary.

        Returns:
            Dictionary representation of the list response.
        """
        return {
            "result": self.result,
            "time": self.time.to_dict(),
        }


@dataclass(**frozen_dataclass_kwargs(repr=False, eq=False))
class BitrixAPIListFastResponse(AbstractBitrixAPIListResponse[JSONGenerator]):
    """
    Fast Bitrix24 list response.

    Stores a lazy one-time generator returned by fast ID-window pagination.
    Items are fetched progressively while the generator is consumed.

    The ``time`` metadata is backed by a mutable raw timing dictionary and
    reflects the current accumulated timing values. Final timing values are
    available only after the result generator has been fully consumed.
    """

    time: InitVar[TimeResponseData]
    _time: TimeResponseData = field(init=False)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"result={self.result}, "
            f"time={self.time})"
        )

    def __post_init__(self, time: TimeResponseData):
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
    def from_dict(cls, json_response: ListFastResponseData, /) -> "BitrixAPIListFastResponse":
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

    def to_dict(self) -> ListFastResponseData:
        """
        Convert fast list response to a dictionary.

        The returned ``result`` keeps the original one-time generator.

        Returns:
            Dictionary representation of the fast list response.
        """
        return {
            "result": self.result,
            "time": self.time.to_dict(),
        }
