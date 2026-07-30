from dataclasses import dataclass
from typing import Annotated, List, Literal, Text, TypedDict

from ...constants.crm import EntityMergeBatchStatus
from ...utils.converters import int_from_bitrix, int_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_schema import BaseSchema

__all__ = [
    "CRMEntityMergeBatch",
    "CRMEntityMergeBatchData",
]


class CRMEntityMergeBatchData(TypedDict):
    STATUS: Annotated[Text, Literal["SUCCESS", "CONFLICT", "ERROR"]]
    ENTITY_IDS: List[int]


@dataclass(**frozen_dataclass_kwargs())
class CRMEntityMergeBatch(BaseSchema[CRMEntityMergeBatchData]):
    """
    Result returned by the ``crm.entity.mergeBatch`` method.

    The method merges several CRM entities of the same type into the first
    entity from the requested ID list and returns operation status with deleted
    entity IDs.
    """

    status: EntityMergeBatchStatus
    entity_ids: List[int]

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMEntityMergeBatchData, /) -> "CRMEntityMergeBatch":
        """
        Create a CRMEntityMergeBatch schema from Bitrix24 merge result data.

        Args:
            bitrix_data: Raw ``result`` object returned by Bitrix24.

        Returns:
            CRMEntityMergeBatch schema with Python-friendly field names.
        """
        return cls(
            status=EntityMergeBatchStatus(bitrix_data["STATUS"]),
            entity_ids=[
                int_from_bitrix(entity_id, is_required=True)
                for entity_id in bitrix_data["ENTITY_IDS"]
            ],
        )

    def to_bitrix(self) -> CRMEntityMergeBatchData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 merge result field names.
        """
        return {
            "STATUS": self.status.value,
            "ENTITY_IDS": [
                int_to_bitrix(entity_id, is_required=True)
                for entity_id in self.entity_ids
            ],
        }
