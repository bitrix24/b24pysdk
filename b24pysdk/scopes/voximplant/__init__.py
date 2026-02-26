from functools import cached_property

from .._base_scope import BaseScope
from .statistic import Statistic

__all__ = [
    "Voximplant",
]


class Voximplant(BaseScope):
    """"""

    @cached_property
    def statistic(self) -> Statistic:
        """"""
        return Statistic(self)
