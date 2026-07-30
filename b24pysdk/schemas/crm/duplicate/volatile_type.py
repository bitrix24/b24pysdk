from dataclasses import dataclass
from typing import Annotated, List, Literal, Text, TypedDict

from ....utils.converters import int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
from ....utils.dataclasses import frozen_dataclass_kwargs
from ..._base_schema import BaseSchema

__all__ = [
    "CRMDuplicateVolatileType",
    "CRMDuplicateVolatileTypeData",
    "CRMDuplicateVolatileTypeField",
    "CRMDuplicateVolatileTypeFieldData",
    "CRMDuplicateVolatileTypeFieldsData",
    "CRMDuplicateVolatileTypesData",
]


class CRMDuplicateVolatileTypeFieldData(TypedDict):
    entityTypeId: Annotated[int, Literal[1, 3, 4]]
    fieldCode: Text
    fieldTitle: Text


CRMDuplicateVolatileTypeFieldsData = List[CRMDuplicateVolatileTypeFieldData]


@dataclass(**frozen_dataclass_kwargs())
class CRMDuplicateVolatileTypeField(BaseSchema[CRMDuplicateVolatileTypeFieldData]):
    """
    Field that can be used for duplicate search.

    Returned by ``crm.duplicate.volatileType.fields``.
    """

    entity_type_id: Annotated[int, Literal[1, 3, 4]]
    field_code: Text
    field_title: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMDuplicateVolatileTypeFieldData, /) -> "CRMDuplicateVolatileTypeField":
        """
        Create a CRMDuplicateVolatileTypeField schema from Bitrix24 data.

        Args:
            bitrix_data: Raw duplicate volatile type field data.

        Returns:
            CRMDuplicateVolatileTypeField schema with Python-friendly field names.
        """
        return cls(
            entity_type_id=int_from_bitrix(bitrix_data["entityTypeId"], is_required=True),
            field_code=text_from_bitrix(bitrix_data["fieldCode"], is_required=True),
            field_title=text_from_bitrix(bitrix_data["fieldTitle"], is_required=True),
        )

    def to_bitrix(self) -> CRMDuplicateVolatileTypeFieldData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 duplicate volatile type field names.
        """
        return {
            "entityTypeId": int_to_bitrix(self.entity_type_id, is_required=True),
            "fieldCode": text_to_bitrix(self.field_code, is_required=True),
            "fieldTitle": text_to_bitrix(self.field_title, is_required=True),
        }


class CRMDuplicateVolatileTypeData(TypedDict):
    id: int
    entityTypeId: Annotated[int, Literal[1, 3, 4]]
    fieldCode: Text


CRMDuplicateVolatileTypesData = List[CRMDuplicateVolatileTypeData]


@dataclass(**frozen_dataclass_kwargs())
class CRMDuplicateVolatileType(BaseSchema[CRMDuplicateVolatileTypeData]):
    """
    Field already registered for duplicate search.

    Returned by ``crm.duplicate.volatileType.list``.
    """

    bitrix_id: int
    entity_type_id: Annotated[int, Literal[1, 3, 4]]
    field_code: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMDuplicateVolatileTypeData, /) -> "CRMDuplicateVolatileType":
        """
        Create a CRMDuplicateVolatileType schema from Bitrix24 data.

        Args:
            bitrix_data: Raw duplicate volatile type data.

        Returns:
            CRMDuplicateVolatileType schema with Python-friendly field names.
        """
        return cls(
            bitrix_id=int_from_bitrix(bitrix_data["id"], is_required=True),
            entity_type_id=int_from_bitrix(bitrix_data["entityTypeId"], is_required=True),
            field_code=text_from_bitrix(bitrix_data["fieldCode"], is_required=True),
        )

    def to_bitrix(self) -> CRMDuplicateVolatileTypeData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 duplicate volatile type field names.
        """
        return {
            "id": int_to_bitrix(self.bitrix_id, is_required=True),
            "entityTypeId": int_to_bitrix(self.entity_type_id, is_required=True),
            "fieldCode": text_to_bitrix(self.field_code, is_required=True),
        }
