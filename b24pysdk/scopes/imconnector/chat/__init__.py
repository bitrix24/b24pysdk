from functools import cached_property

from ..._base_entity import BaseEntity
from .name import Name

__all__ = [
    "Chat",
]


class Chat(BaseEntity):
    """"""

    @cached_property
    def name(self) -> Name:
        """"""
        return Name(self)
