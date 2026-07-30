from functools import cached_property

from ...._base_entity import BaseEntity
from .backlog import Backlog
from .epic import Epic
from .kanban import Kanban
from .sprint import Sprint
from .task import Task

__all__ = [
    "Scrum",
]


class Scrum(BaseEntity):
    """"""

    @cached_property
    def backlog(self) -> Backlog:
        """"""
        return Backlog(self)

    @cached_property
    def epic(self) -> Epic:
        """"""
        return Epic(self)

    @cached_property
    def kanban(self) -> Kanban:
        """"""
        return Kanban(self)

    @cached_property
    def sprint(self) -> Sprint:
        """"""
        return Sprint(self)

    @cached_property
    def task(self) -> Task:
        """"""
        return Task(self)
