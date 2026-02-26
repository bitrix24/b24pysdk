from functools import cached_property

from ..._base_entity import BaseEntity
from .workgroup import Workgroup

__all__ = [
    "API",
]


class API(BaseEntity):
    """"""

    @cached_property
    def workgroup(self) -> Workgroup:
        """"""
        return Workgroup(self)
