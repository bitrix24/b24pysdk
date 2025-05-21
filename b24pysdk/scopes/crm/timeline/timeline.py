from ..base_crm import BaseCRM

from .bindings import Bindings
from .comment import Comment
from .note import Note


class Timeline(BaseCRM):
    """"""

    @property
    def bindings(self) -> Bindings:
        """"""
        return Bindings(self)

    @property
    def comment(self) -> Comment:
        """"""
        return Comment(self)

    @property
    def note(self) -> Note:
        """"""
        return Note(self)
