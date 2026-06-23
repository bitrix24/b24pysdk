from dataclasses import dataclass
from typing import Generic, Type, TypedDict, TypeVar

from ..utils.dataclasses import frozen_dataclass_kwargs
from ._base_schema import BaseSchema

__all__ = [
    "UnbindData",
    "UnbindSchema",
]

_UST = TypeVar("_UST", bound="UnbindSchema")
_USDataT = TypeVar("_USDataT", bound="UnbindData")


class UnbindData(TypedDict):
    count: int


@dataclass(**frozen_dataclass_kwargs())
class UnbindSchema(BaseSchema[_USDataT], Generic[_USDataT]):
    """
    Common result returned by ``*.unbind`` methods.

    The method removes registered handlers and returns the resulting
    operation count.
    """

    count: int

    @classmethod
    def from_bitrix(cls: Type[_UST], bitrix_data: _USDataT, /) -> _UST:
        """
        Create an Unbind schema from Bitrix24 unbind data.

        Args:
            bitrix_data: Raw ``result`` object returned by a Bitrix24
                ``*.unbind`` method.

        Returns:
            Unbind schema with Python-friendly fields.
        """
        return cls(
            count=bitrix_data["count"],
        )

    def to_bitrix(self) -> _USDataT:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 unbind result fields.
        """
        return {
            "count": self.count,
        }
