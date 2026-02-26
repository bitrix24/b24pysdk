from functools import cached_property

from .._base_scope import BaseScope
from .message import Message
from .sender import Sender

__all__ = [
    "Messageservice",
]


class Messageservice(BaseScope):
    """"""

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @cached_property
    def sender(self) -> Sender:
        """"""
        return Sender(self)
