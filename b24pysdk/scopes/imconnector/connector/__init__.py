from functools import cached_property

from ..._base_entity import BaseEntity
from .data import Data

__all__ = [
    "Connector",
]


class Connector(BaseEntity):
    """"""

    @cached_property
    def data(self) -> Data:
        """"""
        return Data(self)
