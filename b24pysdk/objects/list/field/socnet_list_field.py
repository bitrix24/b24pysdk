from typing import TYPE_CHECKING, Generic, TypeVar

from ....constants.list import ListIBlockType
from ._base_list_field import BaseListField, BaseListFieldManager

if TYPE_CHECKING:
    from ....utils.types import Self

__all__ = [
    "SocnetListField",
    "SocnetListFieldManager",
]


class SocnetListField(BaseListField):
    """Field of a Bitrix24 social-network list."""

    IBLOCK_TYPE_ID = ListIBlockType.LISTS_SOCNET

    objects: "SocnetListFieldManager[Self]"


_SocnetListFieldT = TypeVar("_SocnetListFieldT", bound=SocnetListField)


class SocnetListFieldManager(
        BaseListFieldManager[_SocnetListFieldT],
        Generic[_SocnetListFieldT],
):
    """Manager for Bitrix24 social-network list fields."""

    __slots__ = ()


SocnetListField.objects = SocnetListFieldManager()
