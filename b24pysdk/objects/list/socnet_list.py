from typing import TYPE_CHECKING, Generic, Text, TypeVar

from ...constants.list import ListIBlockType
from .._fields import ObjectField
from ._base_list import BaseList, BaseListManager

if TYPE_CHECKING:
    from ...utils.types import Self
    from ..sonet_group import SonetGroup  # noqa: F401

__all__ = [
    "SocnetList",
    "SocnetListManager",
]


class SocnetList(BaseList):
    """Bitrix24 social-network group list."""

    IBLOCK_TYPE_ID = ListIBlockType.LISTS_SOCNET

    objects: "SocnetListManager[Self]"

    socnet_group = ObjectField["SonetGroup"](BaseList.socnet_group_id, object_class="sonet_group")

    @property
    def url(self) -> Text:
        """Return the absolute Bitrix24 group-list URL."""

        if self.socnet_group_id is None:
            raise ValueError("SOCNET_GROUP_ID is required to build the group-list URL.")

        return f"{self._base_url}/workgroups/group/{self.socnet_group_id}/lists/{self.bitrix_pk}/view/0/"


_SocnetListT = TypeVar("_SocnetListT", bound=SocnetList)


class SocnetListManager(BaseListManager[_SocnetListT], Generic[_SocnetListT]):
    """Manager for Bitrix24 social-network group lists."""

    __slots__ = ()


SocnetList.objects = SocnetListManager()
