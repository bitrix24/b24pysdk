from functools import cached_property

from .._base_scope import BaseScope
from .connector import Connector
from .dataset import Dataset
from .source import Source

__all__ = [
    "Biconnector",
]


class Biconnector(BaseScope):
    """"""

    @cached_property
    def connector(self) -> Connector:
        """"""
        return Connector(self)

    @cached_property
    def dataset(self) -> Dataset:
        """"""
        return Dataset(self)

    @cached_property
    def source(self) -> Source:
        """"""
        return Source(self)
