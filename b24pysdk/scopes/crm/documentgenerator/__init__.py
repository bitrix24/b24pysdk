from functools import cached_property

from .._base_crm import BaseCRM
from .document import Document
from .numerator import Numerator
from .template import Template

__all__ = [
    "Documentgenerator",
]


class Documentgenerator(BaseCRM):
    """"""

    @cached_property
    def document(self) -> Document:
        """"""
        return Document(self)

    @cached_property
    def numerator(self) -> Numerator:
        """"""
        return Numerator(self)

    @cached_property
    def template(self) -> Template:
        return Template(self)
