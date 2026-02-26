from functools import cached_property

from .._base_scope import BaseScope
from .checklistitem import Checklistitem
from .commentitem import Commentitem
from .dependence import Dependence
from .elapseditem import Elapseditem
from .item import Item
from .planner import Planner
from .stages import Stages

__all__ = [
    "Task",
]


class Task(BaseScope):
    """"""

    @cached_property
    def checklistitem(self) -> Checklistitem:
        """"""
        return Checklistitem(self)

    @cached_property
    def commentitem(self) -> Commentitem:
        """"""
        return Commentitem(self)

    @cached_property
    def dependence(self) -> Dependence:
        """"""
        return Dependence(self)

    @cached_property
    def elapseditem(self) -> Elapseditem:
        """"""
        return Elapseditem(self)

    @cached_property
    def item(self) -> Item:
        """"""
        return Item(self)

    @cached_property
    def planner(self) -> Planner:
        """"""
        return Planner(self)

    @cached_property
    def stages(self) -> Stages:
        """"""
        return Stages(self)
