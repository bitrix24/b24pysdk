from functools import cached_property

from ..._base_entity import BaseEntity
from .session import Session

__all__ = [
    "Bot",
]


class Bot(BaseEntity):
    """"""

    @cached_property
    def session(self) -> Session:
        """"""
        return Session(self)
