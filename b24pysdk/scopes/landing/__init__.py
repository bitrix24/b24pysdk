from functools import cached_property

from .._base_scope import BaseScope
from .landing import Landing as LandingEntity

__all__ = [
    "Landing",
]


class Landing(BaseScope):
    """"""

    @cached_property
    def landing(self) -> LandingEntity:
        """"""
        return LandingEntity(self)
