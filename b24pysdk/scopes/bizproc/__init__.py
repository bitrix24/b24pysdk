from functools import cached_property

from .._base_scope import BaseScope
from .activity import Activity
from .event import Event
from .robot import Robot
from .task import Task
from .workflow import Workflow

__all__ = [
    "Bizproc",
]


class Bizproc(BaseScope):
    """"""

    @cached_property
    def activity(self) -> Activity:
        """"""
        return Activity(self)

    @cached_property
    def event(self) -> Event:
        """"""
        return Event(self)

    @cached_property
    def robot(self) -> Robot:
        """"""
        return Robot(self)

    @cached_property
    def task(self) -> Task:
        """"""
        return Task(self)

    @cached_property
    def workflow(self) -> Workflow:
        """"""
        return Workflow(self)
