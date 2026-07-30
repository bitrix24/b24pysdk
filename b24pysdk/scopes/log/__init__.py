from functools import cached_property

from .._base_scope import BaseScope
from .blogpost import Blogpost

__all__ = [
    "Log",
]


class Log(BaseScope):
    """"""

    @cached_property
    def blogpost(self) -> Blogpost:
        """"""
        return Blogpost(self)
