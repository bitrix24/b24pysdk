from functools import cached_property

from .._base_scope import BaseScope
from .application import Application

__all__ = [
    "Pull",
]


class Pull(BaseScope):
    """"""

    @cached_property
    def application(self) -> Application:
        """"""
        return Application(self)
