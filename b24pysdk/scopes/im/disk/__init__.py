from functools import cached_property

from ..._base_entity import BaseEntity
from .file import File
from .folder import Folder

__all__ = [
    "Disk",
]


class Disk(BaseEntity):
    """"""

    @cached_property
    def file(self) -> File:
        """"""
        return File(self)

    @cached_property
    def folder(self) -> Folder:
        """"""
        return Folder(self)
