from functools import cached_property

from ..._base_scope import BaseScope
from .employee import Employee
from .node import Node

__all__ = [
    "Humanresources",
]


class Humanresources(BaseScope):
    """"""

    @cached_property
    def employee(self) -> Employee:
        """"""
        return Employee(self)

    @cached_property
    def node(self) -> Node:
        """"""
        return Node(self)
