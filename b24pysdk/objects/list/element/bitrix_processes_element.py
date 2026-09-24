from typing import TYPE_CHECKING, Generic, Text, TypeVar

from ....constants.list import ListIBlockType
from ..._fields import ObjectField
from ._base_list_element import BaseListElement, BaseListElementManager

if TYPE_CHECKING:
    from ....utils.types import Self
    from ..section.bitrix_processes_section import BitrixProcessesSection  # noqa: F401

__all__ = [
    "BitrixProcessesElement",
    "BitrixProcessesElementManager",
]


class BitrixProcessesElement(BaseListElement):
    """Element of a Bitrix24 business-process list."""

    IBLOCK_TYPE_ID = ListIBlockType.BITRIX_PROCESSES

    objects: "BitrixProcessesElementManager[Self]"

    iblock_section = ObjectField["BitrixProcessesSection"](
        BaseListElement.iblock_section_id,
        object_class="list.section",
        discriminator=(IBLOCK_TYPE_ID, None),
    )

    @property
    def url(self) -> Text:
        """Return the absolute Bitrix24 business-process element URL."""

        if self.IBLOCK_ID is None:
            raise ValueError("IBLOCK_ID is required to build the business-process element URL.")

        return f"{self._base_url}/bizproc/processes/{self.IBLOCK_ID}/element/0/{self.bitrix_pk}/"


_BitrixProcessesElementT = TypeVar("_BitrixProcessesElementT", bound=BitrixProcessesElement)


class BitrixProcessesElementManager(BaseListElementManager[_BitrixProcessesElementT], Generic[_BitrixProcessesElementT]):
    """Manager for Bitrix24 business-process list elements."""

    __slots__ = ()


BitrixProcessesElement.objects = BitrixProcessesElementManager()
