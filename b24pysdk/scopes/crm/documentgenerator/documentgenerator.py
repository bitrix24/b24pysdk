from ..base_crm import BaseCRM
from .document import Document
from .numerator import Numerator
from .template import Template


class Documentgenerator(BaseCRM):
    """"""

    @property
    def document(self) -> Document:
        """"""
        return Document(self)

    @property
    def numerator(self) -> Numerator:
        """"""
        return Numerator(self)

    @property
    def template(self) -> Template:
        return Template(self)
