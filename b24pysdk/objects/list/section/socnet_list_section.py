from typing import TYPE_CHECKING, Generic, TypeVar

from ....constants.list import ListIBlockType
from ..._fields import ObjectField
from ._base_list_section import BaseListSection, BaseListSectionManager

if TYPE_CHECKING:
    from ....utils.types import Self

__all__ = [
    "SocnetListSection",
    "SocnetListSectionManager",
]


class SocnetListSection(BaseListSection):
    """Section of a Bitrix24 social-network group list."""

    IBLOCK_TYPE_ID = ListIBlockType.LISTS_SOCNET

    objects: "SocnetListSectionManager[Self]"

    parent_section = ObjectField["SocnetListSection"](
        BaseListSection.parent_section_id,
        object_class="list.section",
        discriminator=(IBLOCK_TYPE_ID, None),
    )


_SocnetListSectionT = TypeVar("_SocnetListSectionT", bound=SocnetListSection)


class SocnetListSectionManager(BaseListSectionManager[_SocnetListSectionT], Generic[_SocnetListSectionT]):
    """Manager for Bitrix24 social-network group list sections."""

    __slots__ = ()


SocnetListSection.objects = SocnetListSectionManager()
