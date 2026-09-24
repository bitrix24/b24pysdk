from functools import cached_property

from ...._base_entity import BaseEntity
from .document import Document

__all__ = [
    "Hcmlink",
]


class Hcmlink(BaseEntity):
    """"""

    @cached_property
    def document(self) -> Document:
        """"""
        return Document(self)
