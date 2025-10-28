from functools import cached_property

from ..._base_crm import BaseCRM
from .blocks import Blocks

__all__ = [
    "Layout",
]


class Layout(BaseCRM):
    """"""

    @cached_property
    def blocks(self) -> Blocks:
        """"""
        return Blocks(self)
