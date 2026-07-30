from functools import cached_property

from ..._base_scope import BaseScope
from .task import Task

__all__ = [
    "Tasks",
]


class Tasks(BaseScope):
    """"""

    @cached_property
    def task(self) -> Task:
        """"""
        return Task(self)
