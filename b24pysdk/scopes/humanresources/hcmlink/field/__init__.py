from functools import cached_property

from ...._base_entity import BaseEntity
from .value import Value

__all__ = [
    "Field",
]


class Field(BaseEntity):
    """"""

    @cached_property
    def value(self) -> Value:
        """"""
        return Value(self)
