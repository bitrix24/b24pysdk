from dataclasses import dataclass
from typing import List, Optional, TypedDict

from ....utils.dataclasses import frozen_dataclass_kwargs
from ..._base_schema import BaseSchema

__all__ = [
    "CRMDuplicateFindByComm",
    "CRMDuplicateFindByCommData",
]


class CRMDuplicateFindByCommData(TypedDict, total=False):
    LEAD: List[int]
    CONTACT: List[int]
    COMPANY: List[int]


@dataclass(**frozen_dataclass_kwargs())
class CRMDuplicateFindByComm(BaseSchema[CRMDuplicateFindByCommData]):
    """
    Duplicate search result returned by ``crm.duplicate.findbycomm``.

    The method returns entity identifiers grouped by CRM entity type.
    """

    lead_ids: Optional[List[int]]
    contact_ids: Optional[List[int]]
    company_ids: Optional[List[int]]

    @classmethod
    def from_bitrix(cls, bitrix_data: CRMDuplicateFindByCommData, /) -> "CRMDuplicateFindByComm":
        """
        Create a CRMDuplicateFindByComm schema from Bitrix24 duplicate data.

        Args:
            bitrix_data: Raw duplicate search result data.

        Returns:
            CRMDuplicateFindByComm schema with Python-friendly field names.
        """
        return cls(
            lead_ids=bitrix_data.get("LEAD"),
            contact_ids=bitrix_data.get("CONTACT"),
            company_ids=bitrix_data.get("COMPANY"),
        )

    def to_bitrix(self) -> CRMDuplicateFindByCommData:
        """
        Convert the schema back to a Bitrix-compatible dictionary.

        Returns:
            Dictionary with Bitrix24 duplicate search result field names.
        """

        bitrix_data: CRMDuplicateFindByCommData = {}

        if self.lead_ids is not None:
            bitrix_data["LEAD"] = self.lead_ids

        if self.contact_ids is not None:
            bitrix_data["CONTACT"] = self.contact_ids

        if self.company_ids is not None:
            bitrix_data["COMPANY"] = self.company_ids

        return bitrix_data
