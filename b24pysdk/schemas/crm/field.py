from dataclasses import dataclass
from typing import Dict, List, Optional, Text, TypedDict

from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import JSONDict
from .._base_schema import BaseSchema
from .._base_schema_dict import BaseSchemaDict

__all__ = [
    "CRMField",
    "CRMFieldData",
    "CRMFieldItem",
    "CRMFieldItemData",
    "CRMFieldsData",
    "CRMFieldsDict",
    "CRMFieldsResultData",
]


class CRMFieldItemData(TypedDict):
    ID: int
    VALUE: Text


@dataclass(**frozen_dataclass_kwargs())
class CRMFieldItem(BaseSchema[CRMFieldItemData]):
    """
    Single item of a CRM field description.
    """

    bitrix_id: int
    value: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMFieldItemData, /) -> "CRMFieldItem":
        """
        Create a CRMFieldItem schema from Bitrix24 CRM field item data.

        Args:
            bitrix_data: Raw CRM field item data.

        Returns:
            CRMFieldItem schema with Python-friendly fields.
        """
        return cls(
            bitrix_id=int(bitrix_data["ID"]),
            value=bitrix_data["VALUE"],
        )

    def to_bitrix(self) -> CRMFieldItemData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM field item names.
        """
        return {
            "ID": self.bitrix_id,
            "VALUE": self.value,
        }


class _CRMFieldOptionalData(TypedDict, total=False):
    isDeprecated: bool
    statusType: Text
    items: List[CRMFieldItemData]
    listLabel: Text
    formLabel: Text
    filerLabel: Text
    upperName: Text
    settings: JSONDict


class CRMFieldData(_CRMFieldOptionalData):
    type: Text
    isRequired: bool
    isReadOnly: bool
    isImmutable: bool
    isMultiple: bool
    isDynamic: bool
    title: Text


@dataclass(**frozen_dataclass_kwargs())
class CRMField(BaseSchema[CRMFieldData]):
    """
    Single CRM field description in ``crm_rest_field_description`` format.
    """

    type: Text
    is_required: bool
    is_read_only: bool
    is_immutable: bool
    is_multiple: bool
    is_dynamic: bool
    title: Text
    is_deprecated: Optional[bool]
    status_type: Optional[Text]
    items: Optional[List[CRMFieldItem]]
    list_label: Optional[Text]
    form_label: Optional[Text]
    filer_label: Optional[Text]
    upper_name: Optional[Text]
    settings: Optional[JSONDict]

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMFieldData, /) -> "CRMField":
        """
        Create a CRMField schema from Bitrix24 CRM field description data.

        Args:
            bitrix_data: Raw CRM field description in
                ``crm_rest_field_description`` format.

        Returns:
            CRMField schema with Python-friendly field names.
        """
        return cls(
            type=bitrix_data["type"],
            is_required=bitrix_data["isRequired"],
            is_read_only=bitrix_data["isReadOnly"],
            is_immutable=bitrix_data["isImmutable"],
            is_multiple=bitrix_data["isMultiple"],
            is_dynamic=bitrix_data["isDynamic"],
            title=bitrix_data["title"],
            is_deprecated=bitrix_data.get("isDeprecated"),
            status_type=bitrix_data.get("statusType"),
            items=[CRMFieldItem.from_bitrix(item_data) for item_data in bitrix_data["items"]] if "items" in bitrix_data else None,
            list_label=bitrix_data.get("listLabel"),
            form_label=bitrix_data.get("formLabel"),
            filer_label=bitrix_data.get("filerLabel"),
            upper_name=bitrix_data.get("upperName"),
            settings=bitrix_data.get("settings"),
        )

    def to_bitrix(self) -> CRMFieldData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM field description names.
        """

        bitrix_data: CRMFieldData = {
            "type": self.type,
            "isRequired": self.is_required,
            "isReadOnly": self.is_read_only,
            "isImmutable": self.is_immutable,
            "isMultiple": self.is_multiple,
            "isDynamic": self.is_dynamic,
            "title": self.title,
        }

        if self.is_deprecated is not None:
            bitrix_data["isDeprecated"] = self.is_deprecated

        if self.status_type is not None:
            bitrix_data["statusType"] = self.status_type

        if self.items is not None:
            bitrix_data["items"] = [item.to_bitrix() for item in self.items]

        if self.list_label is not None:
            bitrix_data["listLabel"] = self.list_label

        if self.form_label is not None:
            bitrix_data["formLabel"] = self.form_label

        if self.filer_label is not None:
            bitrix_data["filerLabel"] = self.filer_label

        if self.upper_name is not None:
            bitrix_data["upperName"] = self.upper_name

        if self.settings is not None:
            bitrix_data["settings"] = self.settings

        return bitrix_data


class CRMFieldsDict(BaseSchemaDict[CRMField, CRMFieldData]):
    """
    CRM fields descriptions indexed by CRM field name.
    """
    _ITEM_SCHEMA = CRMField
    _WRAPPER = "fields"


CRMFieldsData = Dict[Text, CRMFieldData]


class CRMFieldsResultData(TypedDict):
    fields: CRMFieldsData
