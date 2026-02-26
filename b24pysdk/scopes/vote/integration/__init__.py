from functools import cached_property

from ..._base_entity import BaseEntity
from .im import Im

__all__ = [
    "Integration",
]


class Integration(BaseEntity):
    """"""

    @cached_property
    def im(self) -> Im:
        """"""
        return Im(self)
