from dataclasses import dataclass
from typing import Dict, List, Optional, Text, TypedDict

from ...utils.converters import bool_from_bitrix, int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
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
            bitrix_id=int_from_bitrix(bitrix_data["ID"], is_required=True),
            value=text_from_bitrix(bitrix_data["VALUE"], is_required=True),
        )

    def to_bitrix(self) -> CRMFieldItemData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM field item names.
        """
        return {
            "ID": int_to_bitrix(self.bitrix_id, is_required=True),
            "VALUE": text_to_bitrix(self.value, is_required=True),
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
            type=text_from_bitrix(bitrix_data["type"], is_required=True),
            is_required=bool_from_bitrix(bitrix_data["isRequired"], is_required=True),
            is_read_only=bool_from_bitrix(bitrix_data["isReadOnly"], is_required=True),
            is_immutable=bool_from_bitrix(bitrix_data["isImmutable"], is_required=True),
            is_multiple=bool_from_bitrix(bitrix_data["isMultiple"], is_required=True),
            is_dynamic=bool_from_bitrix(bitrix_data["isDynamic"], is_required=True),
            title=text_from_bitrix(bitrix_data["title"], is_required=True),
            is_deprecated=bool_from_bitrix(bitrix_data.get("isDeprecated")),
            status_type=text_from_bitrix(bitrix_data.get("statusType")),
            items=[CRMFieldItem.from_bitrix(item_data) for item_data in bitrix_data["items"]] if "items" in bitrix_data else None,
            list_label=text_from_bitrix(bitrix_data.get("listLabel")),
            form_label=text_from_bitrix(bitrix_data.get("formLabel")),
            filer_label=text_from_bitrix(bitrix_data.get("filerLabel")),
            upper_name=text_from_bitrix(bitrix_data.get("upperName")),
            settings=bitrix_data.get("settings"),
        )

    def to_bitrix(self) -> CRMFieldData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 CRM field description names.
        """

        bitrix_data: CRMFieldData = {
            "type": text_to_bitrix(self.type, is_required=True),
            "isRequired": bool_from_bitrix(self.is_required, is_required=True),
            "isReadOnly": bool_from_bitrix(self.is_read_only, is_required=True),
            "isImmutable": bool_from_bitrix(self.is_immutable, is_required=True),
            "isMultiple": bool_from_bitrix(self.is_multiple, is_required=True),
            "isDynamic": bool_from_bitrix(self.is_dynamic, is_required=True),
            "title": text_to_bitrix(self.title, is_required=True),
        }

        if self.is_deprecated is not None:
            bitrix_data["isDeprecated"] = bool_from_bitrix(self.is_deprecated, is_required=True)

        if self.status_type is not None:
            bitrix_data["statusType"] = text_to_bitrix(self.status_type, is_required=True)

        if self.items is not None:
            bitrix_data["items"] = [item.to_bitrix() for item in self.items]

        if self.list_label is not None:
            bitrix_data["listLabel"] = text_to_bitrix(self.list_label, is_required=True)

        if self.form_label is not None:
            bitrix_data["formLabel"] = text_to_bitrix(self.form_label, is_required=True)

        if self.filer_label is not None:
            bitrix_data["filerLabel"] = text_to_bitrix(self.filer_label, is_required=True)

        if self.upper_name is not None:
            bitrix_data["upperName"] = text_to_bitrix(self.upper_name, is_required=True)

        if self.settings is not None:
            bitrix_data["settings"] = self.settings

        return bitrix_data


class CRMFieldsDict(BaseSchemaDict[CRMField, CRMFieldData]):
    """
    CRM fields descriptions indexed by CRM field name.
    """
    _VALUE_SCHEMA = CRMField


CRMFieldsData = Dict[Text, CRMFieldData]


class CRMFieldsResultData(TypedDict):
    fields: CRMFieldsData
