from functools import cached_property

from .._base_scope import BaseScope
from .engine import Engine
from .prompt import Prompt

__all__ = [
    "Ai",
]


class Ai(BaseScope):
    """"""

    @cached_property
    def engine(self) -> Engine:
        """"""
        return Engine(self)

    @cached_property
    def prompt(self) -> Prompt:
        """"""
        return Prompt(self)
