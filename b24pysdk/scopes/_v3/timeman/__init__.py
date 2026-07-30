from functools import cached_property

from ..._base_scope import BaseScope
from .record import Record

__all__ = [
    "Timeman",
]


class Timeman(BaseScope):
    """"""

    @cached_property
    def record(self) -> Record:
        """"""
        return Record(self)
