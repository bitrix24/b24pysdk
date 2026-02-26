from functools import cached_property

from ..._base_entity import BaseEntity
from .config import Config
from .event import Event
from .push import Push

__all__ = [
    "Application",
]


class Application(BaseEntity):
    """"""

    @cached_property
    def config(self) -> Config:
        """"""
        return Config(self)

    @cached_property
    def event(self) -> Event:
        """"""
        return Event(self)

    @cached_property
    def push(self) -> Push:
        """"""
        return Push(self)
