from functools import cached_property

from ...._base_entity import BaseEntity
from .service import Service

__all__ = [
    "Extra",
]


class Extra(BaseEntity):
    """"""

    @cached_property
    def config(self) -> Service:
        """"""
        return Service(self)
