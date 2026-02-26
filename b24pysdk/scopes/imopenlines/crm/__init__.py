from functools import cached_property

from ..._base_entity import BaseEntity
from .chat import Chat
from .lead import Lead
from .message import Message

__all__ = [
    "Crm",
]


class Crm(BaseEntity):
    """"""

    @cached_property
    def chat(self) -> Chat:
        """"""
        return Chat(self)

    @cached_property
    def lead(self) -> Lead:
        """"""
        return Lead(self)

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)
