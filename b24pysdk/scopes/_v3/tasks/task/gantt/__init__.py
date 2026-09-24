from functools import cached_property

from ....._base_entity import BaseEntity
from .link import Link

__all__ = [
    "Gantt",
]


class Gantt(BaseEntity):
    """"""

    @cached_property
    def link(self) -> Link:
        """"""
        return Link(self)
