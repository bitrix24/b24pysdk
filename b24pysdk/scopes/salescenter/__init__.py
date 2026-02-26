from functools import cached_property

from .._base_scope import BaseScope
from .payment import Payment

__all__ = [
    "Salescenter",
]


class Salescenter(BaseScope):
    """"""

    @cached_property
    def payment(self) -> Payment:
        """"""
        return Payment(self)
