from functools import cached_property

from ...._base_entity import BaseEntity
from .type import Type

__all__ = [
    "Iblock",
]


class Iblock(BaseEntity):
    """"""

    @cached_property
    def type(self) -> Type:
        """"""
        return Type(self)
