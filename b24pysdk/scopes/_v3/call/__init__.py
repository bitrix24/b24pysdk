from functools import cached_property

from ..._base_scope import BaseScope
from .followup import Followup

__all__ = [
    "Call",
]


class Call(BaseScope):
    """"""

    @cached_property
    def followup(self) -> Followup:
        """"""
        return Followup(self)
