from functools import cached_property

from .._base_scope import BaseScope
from .blogcomment import Blogcomment
from .blogpost import Blogpost

__all__ = [
    "Log",
]


class Log(BaseScope):
    """"""

    @cached_property
    def blogcomment(self) -> Blogcomment:
        """"""
        return Blogcomment(self)

    @cached_property
    def blogpost(self) -> Blogpost:
        """"""
        return Blogpost(self)
