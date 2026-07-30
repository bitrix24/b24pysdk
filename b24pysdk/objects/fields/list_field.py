from typing import TYPE_CHECKING, List, Optional, Type, Union

from .int_field import IntField

if TYPE_CHECKING:
    from .._base_object import BaseObject

__all__ = [
    "ListField",
]


class ListField(IntField):
    """Bitrix24 list field that exposes selected item ID as ``int``."""

    __slots__ = ()

    if TYPE_CHECKING:
        def __get__(
                self,
                instance: Optional["BaseObject"],
                owner: Type["BaseObject"],
        ) -> Union["ListField", Optional[int], List[int]]: ...
