from typing import TYPE_CHECKING, Generic, TypeVar

from ....constants.list import ListIBlockType
from ._base_list_field import BaseListField, BaseListFieldManager

if TYPE_CHECKING:
    from ....utils.types import Self

__all__ = [
    "BitrixProcessesField",
    "BitrixProcessesFieldManager",
]


class BitrixProcessesField(BaseListField):
    """Field of a Bitrix24 business-process list."""

    IBLOCK_TYPE_ID = ListIBlockType.BITRIX_PROCESSES

    objects: "BitrixProcessesFieldManager[Self]"


_BitrixProcessesFieldT = TypeVar("_BitrixProcessesFieldT", bound=BitrixProcessesField)


class BitrixProcessesFieldManager(
        BaseListFieldManager[_BitrixProcessesFieldT],
        Generic[_BitrixProcessesFieldT],
):
    """Manager for Bitrix24 business-process list fields."""

    __slots__ = ()


BitrixProcessesField.objects = BitrixProcessesFieldManager()
