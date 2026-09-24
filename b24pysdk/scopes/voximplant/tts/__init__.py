from functools import cached_property

from ..._base_entity import BaseEntity
from .voices import Voices

__all__ = [
    "Tts",
]


class Tts(BaseEntity):
    """"""

    @cached_property
    def voices(self) -> Voices:
        """"""
        return Voices(self)
