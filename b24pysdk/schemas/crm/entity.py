from dataclasses import dataclass
from typing import List, Text, TypedDict

from ...constants.crm import EntityMergeBatchStatus
from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_schema import BaseSchema

__all__ = [
    "CRMEntityMergeBatch",
    "CRMEntityMergeBatchData",
]


class CRMEntityMergeBatchData(TypedDict):
    STATUS: Text
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
            entity_ids=bitrix_data["ENTITY_IDS"],
        )

    def to_bitrix(self) -> CRMEntityMergeBatchData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 merge result field names.
        """
        return {
            "STATUS": self.status.value,
            "ENTITY_IDS": self.entity_ids,
        }
