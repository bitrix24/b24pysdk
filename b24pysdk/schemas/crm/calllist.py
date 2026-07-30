from dataclasses import dataclass
from typing import List, Text, TypedDict

from ...utils.converters import int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_schema import BaseSchema

__all__ = [
    "CalllistStatus",
    "CalllistStatusData",
    "CalllistStatusesData",
]


class CalllistStatusData(TypedDict):
    ID: int
    NAME: Text
    SORT: int
    STATUS_ID: Text


CalllistStatusesData = List[CalllistStatusData]


@dataclass(**frozen_dataclass_kwargs())
class CalllistStatus(BaseSchema[CalllistStatusData]):
    """Call list status returned by ``crm.calllist.statuslist``."""

    bitrix_id: int
    name: Text
    sort: int
    status_id: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: CalllistStatusData, /) -> "CalllistStatus":
        """Create a call list status schema from Bitrix24 data."""
        return cls(
            bitrix_id=int_from_bitrix(bitrix_data["ID"], is_required=True),
            name=text_from_bitrix(bitrix_data["NAME"], is_required=True),
            sort=int_from_bitrix(bitrix_data["SORT"], is_required=True),
            status_id=text_from_bitrix(bitrix_data["STATUS_ID"], is_required=True),
        )

    def to_bitrix(self) -> CalllistStatusData:
        """Convert the schema back to a Bitrix-compatible dictionary."""
        return {
            "ID": int_to_bitrix(self.bitrix_id, is_required=True),
            "NAME": text_to_bitrix(self.name, is_required=True),
            "SORT": int_to_bitrix(self.sort, is_required=True),
            "STATUS_ID": text_to_bitrix(self.status_id, is_required=True),
        }
