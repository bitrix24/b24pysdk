from dataclasses import dataclass
from typing import TypedDict

from ..utils.dataclasses import frozen_dataclass_kwargs
from ._base_schema import BaseSchema

__all__ = [
    "MethodGet",
    "MethodGetData",
]


class MethodGetData(TypedDict):
    isExisting: bool
    isAvailable: bool


@dataclass(**frozen_dataclass_kwargs())
class MethodGet(BaseSchema[MethodGetData]):
    """
    Result returned by the ``method.get`` method.

    The method returns whether a REST method exists on the portal and whether
    it is available for the current application permissions.
    """

    is_existing: bool
    is_available: bool

    @classmethod
    def from_bitrix(cls, bitrix_data: MethodGetData, /) -> "MethodGet":
        """
        Create a MethodGet schema from Bitrix24 method.get data.

        Args:
            bitrix_data: Raw ``result`` object returned by the ``method.get`` method.

        Returns:
            MethodGet schema with Python-friendly field names.
        """
        return cls(
            is_existing=bitrix_data["isExisting"],
            is_available=bitrix_data["isAvailable"],
        )

    def to_bitrix(self) -> MethodGetData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 field names.
        """
        return {
            "isExisting": self.is_existing,
            "isAvailable": self.is_available,
        }
