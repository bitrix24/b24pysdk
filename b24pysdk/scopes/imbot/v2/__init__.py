from functools import cached_property
from typing import Text

from ....utils.functional import classproperty
from ..._base_entity import BaseEntity
from .bot import Bot
from .chat import Chat
from .command import Command
from .event import Event
from .file import File
from .revision import Revision

__all__ = [
    "V2",
]


class V2(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "v2"

    @cached_property
    def bot(self) -> Bot:
        """"""
        return Bot(self)

    @cached_property
    def chat(self) -> Chat:
        """"""
        return Chat(self)

    @cached_property
    def command(self) -> Command:
        """"""
        return Command(self)

    @cached_property
    def event(self) -> Event:
        """"""
        return Event(self)

    @cached_property
    def file(self) -> File:
        """"""
        return File(self)

    @cached_property
    def revision(self) -> Revision:
        """"""
        return Revision(self)
