from functools import cached_property

from ..._base_entity import BaseEntity
from .quick import Quick
from .session import Session

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """"""

    @cached_property
    def quick(self) -> Quick:
        """"""
        return Quick(self)

    @cached_property
    def session(self) -> Session:
        """"""
        return Session(self)
