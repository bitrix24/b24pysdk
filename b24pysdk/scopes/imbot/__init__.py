from functools import cached_property

from .._base_scope import BaseScope
from .v2 import V2

__all__ = [
    "Imbot",
]


class Imbot(BaseScope):
    """"""

    @cached_property
    def v2(self) -> V2:
        """"""
        return V2(self)
