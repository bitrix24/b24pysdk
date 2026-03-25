from functools import cached_property

from ....utils.functional import classproperty
from ..._base_entity import BaseEntity
from .im import Im

__all__ = [
    "Integration",
]


class Integration(BaseEntity):
    """"""

    @classproperty
    def _name(cls):
        return "Integration"

    @cached_property
    def im(self) -> Im:
        """"""
        return Im(self)
