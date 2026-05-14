from functools import cached_property

from .._base_crm import BaseCRM
from .trace import Trace

__all__ = [
    "Tracking",
]


class Tracking(BaseCRM):
    """"""

    @cached_property
    def trace(self) -> Trace:
        """"""
        return Trace(self)
