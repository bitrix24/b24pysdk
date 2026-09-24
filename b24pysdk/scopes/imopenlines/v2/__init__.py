from functools import cached_property
from typing import Text

from ....utils.functional import classproperty
from ..._base_entity import BaseEntity
from .operator import Operator
from .session import Session
from .stat import Stat

__all__ = [
    "V2",
]


class V2(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "v2"

    @cached_property
    def operator(self) -> Operator:
        """"""
        return Operator(self)

    @cached_property
    def session(self) -> Session:
        """"""
        return Session(self)

    @cached_property
    def stat(self) -> Stat:
        """"""
        return Stat(self)
