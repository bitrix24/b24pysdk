from typing import TYPE_CHECKING, Generic, Text, TypeVar

from ...constants.list import ListIBlockType
from ._base_list import BaseList, BaseListManager

if TYPE_CHECKING:
    from ...utils.types import Self

__all__ = [
    "BitrixProcesses",
    "BitrixProcessesManager",
]


class BitrixProcesses(BaseList):
    """Bitrix24 business-process list."""

    IBLOCK_TYPE_ID = ListIBlockType.BITRIX_PROCESSES

    objects: "BitrixProcessesManager[Self]"

    @property
    def url(self) -> Text:
        """Return the absolute Bitrix24 business-process list URL."""
        return f"{self._base_url}/bizproc/processes/{self.bitrix_pk}/view/0/"


_BitrixProcessesT = TypeVar("_BitrixProcessesT", bound=BitrixProcesses)


class BitrixProcessesManager(BaseListManager[_BitrixProcessesT], Generic[_BitrixProcessesT]):
    """Manager for Bitrix24 business-process lists."""

    __slots__ = ()


BitrixProcesses.objects = BitrixProcessesManager()
