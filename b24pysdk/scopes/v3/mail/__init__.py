from functools import cached_property

from ..._base_scope import BaseScope
from .mailbox import Mailbox
from .message import Message
from .recipient import Recipient

__all__ = [
    "Mail",
]


class Mail(BaseScope):
    """"""

    @cached_property
    def mailbox(self) -> Mailbox:
        """"""
        return Mailbox(self)

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @cached_property
    def recipient(self) -> Recipient:
        """"""
        return Recipient(self)
