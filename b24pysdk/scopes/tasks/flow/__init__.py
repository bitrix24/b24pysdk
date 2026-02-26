from functools import cached_property

from ..._base_entity import BaseEntity
from .flow import Flow as _Flow

__all__ = [
    "Flow",
]


class Flow(BaseEntity):
    """"""

    @cached_property
    def flow(self) -> _Flow:
        """"""
        return _Flow(self)
