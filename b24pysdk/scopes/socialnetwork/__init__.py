from functools import cached_property

from .._base_scope import BaseScope
from .api import API

__all__ = [
    "Socialnetwork",
]


class Socialnetwork(BaseScope):
    """"""

    @cached_property
    def api(self) -> API:
        """"""
        return API(self)
