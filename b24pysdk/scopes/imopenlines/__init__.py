from functools import cached_property

from .._base_scope import BaseScope
from .bot import Bot
from .config import Config
from .crm import Crm
from .dialog import Dialog
from .message import Message
from .network import Network
from .operator import Operator
from .revision import Revision
from .session import Session

__all__ = [
    "Imopenlines",
]


class Imopenlines(BaseScope):
    """"""

    @cached_property
    def bot(self) -> Bot:
        """"""
        return Bot(self)

    @cached_property
    def config(self) -> Config:
        """"""
        return Config(self)

    @cached_property
    def crm(self) -> Crm:
        """"""
        return Crm(self)

    @cached_property
    def dialog(self) -> Dialog:
        """"""
        return Dialog(self)

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @cached_property
    def network(self) -> Network:
        """"""
        return Network(self)

    @cached_property
    def operator(self) -> Operator:
        """"""
        return Operator(self)

    @cached_property
    def revision(self) -> Revision:
        """"""
        return Revision(self)

    @cached_property
    def session(self) -> Session:
        """"""
        return Session(self)
