from functools import cached_property

from ..._base_entity import BaseEntity
from .scrum import Scrum

__all__ = [
    "API",
]


class API(BaseEntity):
    """"""

    @cached_property
    def scrum(self) -> Scrum:
        """"""
        return Scrum(self)
