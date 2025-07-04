from ..base_crm import BaseCRM
from .bindings import Bindings
from .comment import Comment
from .logmessage import Logmessage
from .note import Note
from .visual_element import Icon, Logo


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
    def icon(self) -> Icon:
        """"""
        return Icon(self)

    @property
    def logmessage(self) -> Logmessage:
        """"""
        return Logmessage(self)

    @property
    def logo(self) -> Logo:
        """"""
        return Logo(self)

    @property
    def note(self) -> Note:
        """"""
        return Note(self)
