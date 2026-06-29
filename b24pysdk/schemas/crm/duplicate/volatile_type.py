from dataclasses import dataclass
from typing import Annotated, List, Literal, Text, TypedDict

from ....utils.dataclasses import frozen_dataclass_kwargs
from ..._base_listable_schema import BaseListableSchema

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
class CRMDuplicateVolatileTypeField(BaseListableSchema[CRMDuplicateVolatileTypeFieldData]):
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
            entity_type_id=bitrix_data["entityTypeId"],
            field_code=bitrix_data["fieldCode"],
            field_title=bitrix_data["fieldTitle"],
        )

    def to_bitrix(self) -> CRMDuplicateVolatileTypeFieldData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 duplicate volatile type field names.
        """
        return {
            "entityTypeId": self.entity_type_id,
            "fieldCode": self.field_code,
            "fieldTitle": self.field_title,
        }


class CRMDuplicateVolatileTypeData(TypedDict):
    id: int
    entityTypeId: Annotated[int, Literal[1, 3, 4]]
    fieldCode: Text


CRMDuplicateVolatileTypesData = List[CRMDuplicateVolatileTypeData]


@dataclass(**frozen_dataclass_kwargs())
class CRMDuplicateVolatileType(BaseListableSchema[CRMDuplicateVolatileTypeData]):
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
            bitrix_id=bitrix_data["id"],
            entity_type_id=bitrix_data["entityTypeId"],
            field_code=bitrix_data["fieldCode"],
        )

    def to_bitrix(self) -> CRMDuplicateVolatileTypeData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 duplicate volatile type field names.
        """
        return {
            "id": self.bitrix_id,
            "entityTypeId": self.entity_type_id,
            "fieldCode": self.field_code,
        }
