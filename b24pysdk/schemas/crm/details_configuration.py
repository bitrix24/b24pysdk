from dataclasses import dataclass
from typing import List, Optional, Text, TypedDict

from ...utils.converters import bool_from_bitrix, bool_to_bitrix, text_from_bitrix, text_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import JSONDict
from .._base_schema import BaseSchema

__all__ = [
    "CRMDetailsConfigurationElement",
    "CRMDetailsConfigurationElementData",
    "CRMDetailsConfigurationElementsData",
    "CRMDetailsConfigurationSection",
    "CRMDetailsConfigurationSectionData",
    "CRMDetailsConfigurationSectionsData",
]


class _CRMDetailsConfigurationElementOptionalData(TypedDict, total=False):
    optionFlags: int
    options: JSONDict


class CRMDetailsConfigurationElementData(_CRMDetailsConfigurationElementOptionalData):
    name: Text


CRMDetailsConfigurationElementsData = List[CRMDetailsConfigurationElementData]


@dataclass(**frozen_dataclass_kwargs())
class CRMDetailsConfigurationElement(BaseSchema[CRMDetailsConfigurationElementData]):
    """
    Field element inside a CRM details card configuration section.
    """

    name: Text
    option_flags: Optional[bool]
    options: Optional[JSONDict]

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMDetailsConfigurationElementData, /) -> "CRMDetailsConfigurationElement":
        """
        Create a CRMDetailsConfigurationElement schema from Bitrix24 data.
        """
        return cls(
            name=text_from_bitrix(bitrix_data["name"], is_required=True),
            option_flags=bool_from_bitrix(bitrix_data.get("optionFlags")),
            options=bitrix_data.get("options"),
        )

    def to_bitrix(self) -> CRMDetailsConfigurationElementData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.
        """

        bitrix_data: CRMDetailsConfigurationElementData = {
            "name": text_to_bitrix(self.name, is_required=True),
        }

        if self.option_flags is not None:
            bitrix_data["optionFlags"] = bool_to_bitrix(self.option_flags, is_required=True, serialize_as=int)

        if self.options is not None:
            bitrix_data["options"] = self.options

        return bitrix_data


class CRMDetailsConfigurationSectionData(TypedDict):
    name: Text
    title: Text
    type: Text
    elements: CRMDetailsConfigurationElementsData


CRMDetailsConfigurationSectionsData = List[CRMDetailsConfigurationSectionData]


@dataclass(**frozen_dataclass_kwargs())
class CRMDetailsConfigurationSection(BaseSchema[CRMDetailsConfigurationSectionData]):
    """
    Section inside a CRM details card configuration.
    """

    name: Text
    title: Text
    type: Text
    elements: List[CRMDetailsConfigurationElement]

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMDetailsConfigurationSectionData, /) -> "CRMDetailsConfigurationSection":
        """
        Create a CRMDetailsConfigurationSection schema from Bitrix24 data.
        """
        return cls(
            name=text_from_bitrix(bitrix_data["name"], is_required=True),
            title=text_from_bitrix(bitrix_data["title"], is_required=True),
            type=text_from_bitrix(bitrix_data["type"], is_required=True),
            elements=[
                CRMDetailsConfigurationElement.from_bitrix(element_data)
                for element_data in bitrix_data["elements"]
            ],
        )

    def to_bitrix(self) -> CRMDetailsConfigurationSectionData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.
        """
        return {
            "name": text_to_bitrix(self.name, is_required=True),
            "title": text_to_bitrix(self.title, is_required=True),
            "type": text_to_bitrix(self.type, is_required=True),
            "elements": [element.to_bitrix() for element in self.elements],
        }
