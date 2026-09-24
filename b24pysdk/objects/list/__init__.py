from typing import TYPE_CHECKING, Generic, Text, TypeVar

from ...constants.list import ListIBlockType
from ._base_list import BaseList, BaseListManager

if TYPE_CHECKING:
    from ...utils.types import Self

__all__ = [
    "List",
    "ListManager",
]


class List(BaseList):
    """Bitrix24 universal list."""

    IBLOCK_TYPE_ID = ListIBlockType.LISTS

    objects: "ListManager[Self]"

    @property
    def url(self) -> Text:
        """Return the absolute Bitrix24 list URL."""
        return f"{self._base_url}/company/lists/{self.bitrix_pk}/view/0/"


_ListT = TypeVar("_ListT", bound=List)


class ListManager(BaseListManager[_ListT], Generic[_ListT]):
    """Manager for Bitrix24 universal lists."""

    __slots__ = ()


List.objects = ListManager()
