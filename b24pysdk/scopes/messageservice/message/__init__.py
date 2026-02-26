from functools import cached_property

from ..._base_entity import BaseEntity
from .status import Status

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """"""

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)
