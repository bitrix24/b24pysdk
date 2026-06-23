from dataclasses import dataclass
from typing import Dict, Optional, Text, TypedDict

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
            type=bitrix_data["type"],
            is_required=bitrix_data["isRequired"],
            is_read_only=bitrix_data["isReadOnly"],
            title=bitrix_data["title"],
            size=bitrix_data.get("size"),
        )

    def to_bitrix(self) -> VatFieldData:
        """
        Convert the VAT field schema back to Bitrix24 format.
        """

        bitrix_data: VatFieldData = {
            "type": self.type,
            "isRequired": self.is_required,
            "isReadOnly": self.is_read_only,
            "title": self.title,
        }

        if self.size is not None:
            bitrix_data["size"] = self.size

        return bitrix_data


VatFieldsData = Dict[Text, VatFieldData]


class VatFieldsDict(BaseSchemaDict[VatField, VatFieldData]):
    """
    VAT field descriptions indexed by VAT field name.
    """
    _ITEM_SCHEMA = VatField
