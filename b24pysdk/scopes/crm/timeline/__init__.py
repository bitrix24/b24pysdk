from functools import cached_property

from .._base_crm import BaseCRM
from ._images import Icon, Logo
from .bindings import Bindings
from .comment import Comment
from .item import Item
from .layout import Layout
from .logmessage import Logmessage
from .note import Note

__all__ = [
    "Timeline",
]


class Timeline(BaseCRM):
    """"""

    @cached_property
    def bindings(self) -> Bindings:
        """"""
        return Bindings(self)

    @cached_property
    def comment(self) -> Comment:
        """"""
        return Comment(self)

    @cached_property
    def icon(self) -> Icon:
        """"""
        return Icon(self)

    @cached_property
    def item(self) -> Item:
        """"""
        return Item(self)

    @cached_property
    def layout(self) -> Layout:
        """"""
        return Layout(self)

    @cached_property
    def logmessage(self) -> Logmessage:
        """"""
        return Logmessage(self)

    @cached_property
    def logo(self) -> Logo:
        """"""
        return Logo(self)

    @cached_property
    def note(self) -> Note:
        """"""
        return Note(self)

