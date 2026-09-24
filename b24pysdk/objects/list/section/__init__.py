from typing import TYPE_CHECKING, Generic, TypeVar

from ....constants.list import ListIBlockType
from ..._fields import ObjectField
from ._base_list_section import BaseListSection, BaseListSectionManager

if TYPE_CHECKING:
    from ....utils.types import Self

__all__ = [
    "ListSection",
    "ListSectionManager",
]


class ListSection(BaseListSection):
    """Section of a Bitrix24 universal list."""

    IBLOCK_TYPE_ID = ListIBlockType.LISTS

    objects: "ListSectionManager[Self]"

    parent_section = ObjectField["ListSection"](
        BaseListSection.parent_section_id,
        object_class="list.section",
        discriminator=(IBLOCK_TYPE_ID, None),
    )


_ListSectionT = TypeVar("_ListSectionT", bound=ListSection)


class ListSectionManager(BaseListSectionManager[_ListSectionT], Generic[_ListSectionT]):
    """Manager for Bitrix24 universal-list sections."""

    __slots__ = ()


ListSection.objects = ListSectionManager()
