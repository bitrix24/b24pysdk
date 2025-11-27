from functools import cached_property

from .._base_scope import BaseScope
from .attached_object import AttachedObject
from .file import File
from .folder import Folder
from .rights import Rights
from .storage import Storage
from .version import Version

__all__ = [
    "Disk",
]


class Disk(BaseScope):
    """"""

    @cached_property
    def attached_object(self) -> AttachedObject:
        """"""
        return AttachedObject(self)

    @cached_property
    def file(self) -> File:
        """"""
        return File(self)

    @cached_property
    def folder(self) -> Folder:
        """"""
        return Folder(self)

    @cached_property
    def rights(self) -> Rights:
        """"""
        return Rights(self)

    @cached_property
    def storage(self) -> Storage:
        """"""
        return Storage(self)

    @cached_property
    def version(self) -> Version:
        """"""
        return Version(self)
