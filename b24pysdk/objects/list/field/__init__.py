from typing import TYPE_CHECKING, Generic, TypeVar

from ....constants.list import ListIBlockType
from ._base_list_field import BaseListField, BaseListFieldManager

if TYPE_CHECKING:
    from ....utils.types import Self

__all__ = [
    "ListField",
    "ListFieldManager",
]


class ListField(BaseListField):
    """Field of a Bitrix24 universal list."""

    IBLOCK_TYPE_ID = ListIBlockType.LISTS

    objects: "ListFieldManager[Self]"


_ListFieldT = TypeVar("_ListFieldT", bound=ListField)


class ListFieldManager(
        BaseListFieldManager[_ListFieldT],
        Generic[_ListFieldT],
):
    """Manager for Bitrix24 universal-list fields."""

    __slots__ = ()


ListField.objects = ListFieldManager()
