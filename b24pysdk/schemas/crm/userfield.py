from dataclasses import dataclass
from typing import List, Text, TypedDict

from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_listable_schema import BaseListableSchema

__all__ = [
    "CRMUserfieldType",
    "CRMUserfieldTypeData",
    "CRMUserfieldTypesData",
]


class CRMUserfieldTypeData(TypedDict):
    ID: Text
    title: Text


CRMUserfieldTypesData = List[CRMUserfieldTypeData]


@dataclass(**frozen_dataclass_kwargs())
class CRMUserfieldType(BaseListableSchema[CRMUserfieldTypeData]):
    """User field type returned by ``crm.userfield.types``."""

    bitrix_id: Text
    title: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMUserfieldTypeData, /) -> "CRMUserfieldType":
        """Create a user field type schema from Bitrix24 data."""
        return cls(
            bitrix_id=bitrix_data["ID"],
            title=bitrix_data["title"],
        )

    def to_bitrix(self) -> CRMUserfieldTypeData:
        """Convert the schema back to a Bitrix-compatible dictionary."""
        return {
            "ID": self.bitrix_id,
            "title": self.title,
        }
