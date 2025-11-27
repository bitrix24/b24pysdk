from functools import cached_property

from ..._base_entity import BaseEntity
from .status import Status

__all__ = [
    "Meeting",
]


class Meeting(BaseEntity):
    """"""

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)

