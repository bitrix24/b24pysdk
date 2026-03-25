from functools import cached_property

from .._base_scope import BaseScope
from .comment import Comment
from .fields import Fields
from .item import Item
from .stage import Stage
from .task import Task
from .timeline import Timeline
from .type import Type

__all__ = [
    "Rpa",
]


class Rpa(BaseScope):
    """"""

    @cached_property
    def comment(self) -> Comment:
        """"""
        return Comment(self)

    @cached_property
    def fields(self) -> Fields:
        """"""
        return Fields(self)

    @cached_property
    def item(self) -> Item:
        """"""
        return Item(self)

    @cached_property
    def stage(self) -> Stage:
        """"""
        return Stage(self)

    @cached_property
    def task(self) -> Task:
        """"""
        return Task(self)

    @cached_property
    def timeline(self) -> Timeline:
        """"""
        return Timeline(self)

    @cached_property
    def type(self) -> Type:
        """"""
        return Type(self)
