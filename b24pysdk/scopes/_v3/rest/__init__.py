from functools import cached_property

from ..._base_scope import BaseScope
from .documentation import Documentation
from .scope import Scope

__all__ = [
    "Rest",
]


class Rest(BaseScope):
    """"""

    @cached_property
    def documentation(self) -> Documentation:
        """"""
        return Documentation(self)

    @cached_property
    def scope(self) -> Scope:
        """"""
        return Scope(self)
