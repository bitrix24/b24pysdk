from functools import cached_property

from .._base_scope import BaseScope
from .accessibility import Accessibility
from .event import Event
from .meeting import Meeting
from .resource import Resource
from .section import Section
from .settings import Settings
from .user import User

__all__ = [
    "Calendar",
]


class Calendar(BaseScope):
    """"""

    @cached_property
    def accessibility(self) -> Accessibility:
        """"""
        return Accessibility(self)

    @cached_property
    def event(self) -> Event:
        """"""
        return Event(self)

    @cached_property
    def meeting(self) -> Meeting:
        """"""
        return Meeting(self)

    @cached_property
    def resource(self) -> Resource:
        """"""
        return Resource(self)

    @cached_property
    def section(self) -> Section:
        """"""
        return Section(self)

    @cached_property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)
