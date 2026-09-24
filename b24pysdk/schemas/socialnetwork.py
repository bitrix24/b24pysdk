from typing import List, TypedDict

from ..utils.types import JSONDict

__all__ = [
    "WorkgroupListData",
]


class WorkgroupListData(TypedDict):
    """Raw result returned by ``socialnetwork.api.workgroup.list``."""
    workgroups: List[JSONDict]
