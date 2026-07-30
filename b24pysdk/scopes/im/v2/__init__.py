from functools import cached_property
from typing import Text

from ....utils.functional import classproperty
from ..._base_entity import BaseEntity
from .event import Event
from .file import File

__all__ = [
    "V2",
]


class V2(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "v2"

    @cached_property
    def event(self) -> Event:
        """"""
        return Event(self)

    @cached_property
    def file(self) -> File:
        """"""
        return File(self)
