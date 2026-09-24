from typing import TYPE_CHECKING, Generic, TypeVar

from ....constants.list import ListIBlockType
from ..._fields import ObjectField
from ._base_list_section import BaseListSection, BaseListSectionManager

if TYPE_CHECKING:
    from ....utils.types import Self

__all__ = [
    "BitrixProcessesSection",
    "BitrixProcessesSectionManager",
]


class BitrixProcessesSection(BaseListSection):
    """Section of a Bitrix24 business-process list."""

    IBLOCK_TYPE_ID = ListIBlockType.BITRIX_PROCESSES

    objects: "BitrixProcessesSectionManager[Self]"

    parent_section = ObjectField["BitrixProcessesSection"](
        BaseListSection.parent_section_id,
        object_class="list.section",
        discriminator=(IBLOCK_TYPE_ID, None),
    )


_BitrixProcessesSectionT = TypeVar("_BitrixProcessesSectionT", bound=BitrixProcessesSection)


class BitrixProcessesSectionManager(BaseListSectionManager[_BitrixProcessesSectionT], Generic[_BitrixProcessesSectionT]):
    """Manager for Bitrix24 business-process list sections."""

    __slots__ = ()


BitrixProcessesSection.objects = BitrixProcessesSectionManager()
