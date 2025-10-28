from functools import cached_property

from ..._base_crm import BaseCRM
from .configuration import Configuration

__all__ = [
    "Details",
]


class Details(BaseCRM):
    """"""

    @cached_property
    def configuration(self) -> Configuration:
        """"""
        return Configuration(self)
