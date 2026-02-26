from functools import cached_property

from ..._base_entity import BaseEntity
from .element import Element

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """"""

    @cached_property
    def element(self) -> Element:
        """"""
        return Element(self)
