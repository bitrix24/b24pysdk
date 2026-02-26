from functools import cached_property

from ..._base_entity import BaseEntity
from .userfield import Userfield

__all__ = [
    "Item",
]


class Item(BaseEntity):
    """"""

    @cached_property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)
