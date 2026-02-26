from functools import cached_property

from .._base_scope import BaseScope
from .document import Document
from .numerator import Numerator
from .region import Region
from .role import Role
from .template import Template

__all__ = [
    "Documentgenerator",
]


class Documentgenerator(BaseScope):
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
    def region(self) -> Region:
        """"""
        return Region(self)

    @cached_property
    def role(self) -> Role:
        """"""
        return Role(self)

    @cached_property
    def template(self) -> Template:
        """"""
        return Template(self)
