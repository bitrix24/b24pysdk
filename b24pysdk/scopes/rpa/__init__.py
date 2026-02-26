from functools import cached_property

from .._base_scope import BaseScope
from .task import Task

__all__ = [
    "Rpa",
]


class Rpa(BaseScope):
    """"""

    @cached_property
    def task(self) -> Task:
        """"""
        return Task(self)
