from functools import cached_property

from ..._base_scope import BaseScope
from .collection import Collection
from .document import Document
from .file import File

__all__ = [
    "Note",
]


class Note(BaseScope):
    """"""

    @cached_property
    def collection(self) -> Collection:
        """"""
        return Collection(self)

    @cached_property
    def document(self) -> Document:
        """"""
        return Document(self)

    @cached_property
    def file(self) -> File:
        """"""
        return File(self)
