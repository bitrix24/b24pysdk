from dataclasses import dataclass
from typing import List, Text, TypedDict

from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_listable_schema import BaseListableSchema

__all__ = [
    "RequisitePresetCountriesData",
    "RequisitePresetCountry",
    "RequisitePresetCountryData",
]


class RequisitePresetCountryData(TypedDict):
    ID: int
    CODE: Text
    TITLE: Text


RequisitePresetCountriesData = List[RequisitePresetCountryData]


@dataclass(**frozen_dataclass_kwargs())
class RequisitePresetCountry(BaseListableSchema[RequisitePresetCountryData]):
    """Country item returned by ``crm.requisite.preset.countries``."""

    bitrix_id: int
    code: Text
    title: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: RequisitePresetCountryData, /) -> "RequisitePresetCountry":
        """Create a requisite preset country schema from Bitrix24 data."""
        return cls(
            bitrix_id=int(bitrix_data["ID"]),
            code=bitrix_data["CODE"],
            title=bitrix_data["TITLE"],
        )

    def to_bitrix(self) -> RequisitePresetCountryData:
        """Convert the schema back to a Bitrix-compatible dictionary."""
        return {
            "ID": self.bitrix_id,
            "CODE": self.code,
            "TITLE": self.title,
        }
