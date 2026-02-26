from functools import cached_property

from .._base_scope import BaseScope
from .flow import Flow
from .task import Task

__all__ = [
    "Tasks",
]


class Tasks(BaseScope):
    """"""

    @cached_property
    def flow(self) -> Flow:
        """"""
        return Flow(self)

    @cached_property
    def task(self) -> Task:
        """"""
        return Task(self)
