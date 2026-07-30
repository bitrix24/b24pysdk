from dataclasses import dataclass
from typing import List, Text, TypedDict

from ...utils.converters import int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_schema import BaseSchema

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
class RequisitePresetCountry(BaseSchema[RequisitePresetCountryData]):
    """Country item returned by ``crm.requisite.preset.countries``."""

    bitrix_id: int
    code: Text
    title: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: RequisitePresetCountryData, /) -> "RequisitePresetCountry":
        """Create a requisite preset country schema from Bitrix24 data."""
        return cls(
            bitrix_id=int_from_bitrix(bitrix_data["ID"], is_required=True),
            code=text_from_bitrix(bitrix_data["CODE"], is_required=True),
            title=text_from_bitrix(bitrix_data["TITLE"], is_required=True),
        )

    def to_bitrix(self) -> RequisitePresetCountryData:
        """Convert the schema back to a Bitrix-compatible dictionary."""
        return {
            "ID": int_to_bitrix(self.bitrix_id, is_required=True),
            "CODE": text_to_bitrix(self.code, is_required=True),
            "TITLE": text_to_bitrix(self.title, is_required=True),
        }
