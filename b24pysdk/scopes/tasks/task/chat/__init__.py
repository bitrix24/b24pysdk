from functools import cached_property

from ...._base_entity import BaseEntity
from .message import Message

__all__ = [
    "Chat",
]


class Chat(BaseEntity):
    """"""

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)
