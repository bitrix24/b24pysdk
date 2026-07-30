from dataclasses import dataclass
from typing import Dict, Optional, Text, TypedDict

from ...utils.converters import bool_from_bitrix, text_from_bitrix, text_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_schema import BaseSchema
from .._base_schema_dict import BaseSchemaDict

__all__ = [
    "VatField",
    "VatFieldData",
    "VatFieldsData",
    "VatFieldsDict",
]


class _VatFieldOptionalData(TypedDict, total=False):
    size: Text


class VatFieldData(_VatFieldOptionalData):
    type: Text
    isRequired: bool
    isReadOnly: bool
    title: Text


@dataclass(**frozen_dataclass_kwargs())
class VatField(BaseSchema[VatFieldData]):
    """
    Single VAT field description returned by ``crm.vat.fields``.
    """

    type: Text
    is_required: bool
    is_read_only: bool
    title: Text
    size: Optional[Text]

    @classmethod
    def from_bitrix(cls, bitrix_data: VatFieldData, /) -> "VatField":
        """
        Create a VAT field schema from Bitrix24 data.
        """
        return cls(
            type=text_from_bitrix(bitrix_data["type"], is_required=True),
            is_required=bool_from_bitrix(bitrix_data["isRequired"], is_required=True),
            is_read_only=bool_from_bitrix(bitrix_data["isReadOnly"], is_required=True),
            title=text_from_bitrix(bitrix_data["title"], is_required=True),
            size=text_from_bitrix(bitrix_data.get("size")),
        )

    def to_bitrix(self) -> VatFieldData:
        """
        Convert the VAT field schema back to Bitrix24 format.
        """

        bitrix_data: VatFieldData = {
            "type": text_to_bitrix(self.type, is_required=True),
            "isRequired": bool_from_bitrix(self.is_required, is_required=True),
            "isReadOnly": bool_from_bitrix(self.is_read_only, is_required=True),
            "title": text_to_bitrix(self.title, is_required=True),
        }

        if self.size is not None:
            bitrix_data["size"] = text_to_bitrix(self.size, is_required=True)

        return bitrix_data


VatFieldsData = Dict[Text, VatFieldData]


class VatFieldsDict(BaseSchemaDict[VatField, VatFieldData]):
    """
    VAT field descriptions indexed by VAT field name.
    """
    _VALUE_SCHEMA = VatField
