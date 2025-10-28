from functools import cached_property

from ..item.details import Details as BaseDetails
from .configuration import Configuration

__all__ = [
    "Details",
]


class Details(BaseDetails):
    """"""

    @cached_property
    def configuration(self) -> Configuration:
        """"""
        return Configuration(self)
