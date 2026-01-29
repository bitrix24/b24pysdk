from functools import cached_property

from .._base_scope import BaseScope
from .paysystem import Paysystem

__all__ = [
    "Sale",
]


class Sale(BaseScope):

    @cached_property
    def paysystem(self) -> Paysystem:
        return Paysystem(self)
