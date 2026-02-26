from functools import cached_property

from .._base_scope import BaseScope
from .v1 import V1

__all__ = [
    "Booking",
]


class Booking(BaseScope):
    """"""

    @cached_property
    def v1(self) -> V1:
        """"""
        return V1(self)
