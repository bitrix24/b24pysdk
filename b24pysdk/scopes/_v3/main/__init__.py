from functools import cached_property

from ..._base_scope import BaseScope
from .eventlog import Eventlog

__all__ = [
    "Main",
]


class Main(BaseScope):
    """"""

    @cached_property
    def eventlog(self) -> Eventlog:
        """"""
        return Eventlog(self)
