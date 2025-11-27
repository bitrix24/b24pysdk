from functools import cached_property

from ..._base_entity import BaseEntity
from .settings import Settings

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @cached_property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

