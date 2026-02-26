from functools import cached_property

from .._base_scope import BaseScope
from .b2e import B2e

__all__ = [
    "Sign",
]


class Sign(BaseScope):
    """"""

    @cached_property
    def b2e(self) -> B2e:
        """"""
        return B2e(self)
