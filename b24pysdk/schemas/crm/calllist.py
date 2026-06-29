from dataclasses import dataclass
from typing import List, Text, TypedDict

from ...utils.dataclasses import frozen_dataclass_kwargs
from .._base_listable_schema import BaseListableSchema

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
class CalllistStatus(BaseListableSchema[CalllistStatusData]):
    """Call list status returned by ``crm.calllist.statuslist``."""

    bitrix_id: int
    name: Text
    sort: int
    status_id: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: CalllistStatusData, /) -> "CalllistStatus":
        """Create a call list status schema from Bitrix24 data."""
        return cls(
            bitrix_id=int(bitrix_data["ID"]),
            name=bitrix_data["NAME"],
            sort=int(bitrix_data["SORT"]),
            status_id=bitrix_data["STATUS_ID"],
        )

    def to_bitrix(self) -> CalllistStatusData:
        """Convert the schema back to a Bitrix-compatible dictionary."""
        return {
            "ID": self.bitrix_id,
            "NAME": self.name,
            "SORT": self.sort,
            "STATUS_ID": self.status_id,
        }
