from functools import cached_property

from .._base_scope import BaseScope
from .chat import Chat
from .counters import Counters
from .department import Department
from .dialog import Dialog
from .disk import Disk
from .message import Message
from .notify import Notify
from .recent import Recent
from .revision import Revision
from .search import Search
from .user import User

__all__ = [
    "Im",
]


class Im(BaseScope):
    """"""

    @cached_property
    def chat(self) -> Chat:
        """"""
        return Chat(self)

    @cached_property
    def counters(self) -> Counters:
        """"""
        return Counters(self)

    @cached_property
    def department(self) -> Department:
        """"""
        return Department(self)

    @cached_property
    def dialog(self) -> Dialog:
        """"""
        return Dialog(self)

    @cached_property
    def disk(self) -> Disk:
        """"""
        return Disk(self)

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @cached_property
    def revision(self) -> Revision:
        """"""
        return Revision(self)

    @cached_property
    def notify(self) -> Notify:
        """"""
        return Notify(self)

    @cached_property
    def recent(self) -> Recent:
        """"""
        return Recent(self)

    @cached_property
    def search(self) -> Search:
        """"""
        return Search(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)
