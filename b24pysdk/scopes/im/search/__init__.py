from functools import cached_property

from ..._base_entity import BaseEntity
from .chat import Chat
from .department import Department
from .last import Last
from .user import User

__all__ = [
    "Search",
]


class Search(BaseEntity):
    """"""

    @cached_property
    def chat(self) -> Chat:
        """"""
        return Chat(self)

    @cached_property
    def department(self) -> Department:
        """"""
        return Department(self)

    @cached_property
    def last(self) -> Last:
        """"""
        return Last(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)
