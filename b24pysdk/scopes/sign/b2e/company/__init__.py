from functools import cached_property

from ...._base_entity import BaseEntity
from .provider import Provider

__all__ = [
    "Company",
]


class Company(BaseEntity):
    """"""

    @cached_property
    def provider(self) -> Provider:
        """"""
        return Provider(self)
