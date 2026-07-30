from functools import cached_property
from typing import Text

from ....utils.functional import classproperty
from ..._base_entity import BaseEntity
from .company import Company
from .document import Document
from .mysafe import Mysafe
from .personal import Personal

__all__ = [
    "B2e",
]


class B2e(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "b2e"

    @cached_property
    def company(self) -> Company:
        """"""
        return Company(self)

    @cached_property
    def document(self) -> Document:
        """"""
        return Document(self)

    @cached_property
    def mysafe(self) -> Mysafe:
        """"""
        return Mysafe(self)

    @cached_property
    def personal(self) -> Personal:
        """"""
        return Personal(self)
