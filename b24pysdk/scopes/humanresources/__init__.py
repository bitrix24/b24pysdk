from functools import cached_property

from .._base_scope import BaseScope
from .hcmlink import Hcmlink

__all__ = [
    "Humanresources",
]


class Humanresources(BaseScope):
    """"""

    @cached_property
    def hcmlink(self) -> Hcmlink:
        """"""
        return Hcmlink(self)
