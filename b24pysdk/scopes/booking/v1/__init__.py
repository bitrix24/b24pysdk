from functools import cached_property

from ..._base_entity import BaseEntity
from .booking import Booking
from .clienttype import Clienttype
from .resource import Resource
from .resource_type import ResourceType
from .waitlist import Waitlist

__all__ = [
    "V1",
]


class V1(BaseEntity):
    """"""

    @cached_property
    def booking(self) -> Booking:
        """"""
        return Booking(self)

    @cached_property
    def clienttype(self) -> Clienttype:
        """"""
        return Clienttype(self)

    @cached_property
    def resource(self) -> Resource:
        """"""
        return Resource(self)

    @cached_property
    def resource_type(self) -> ResourceType:
        """"""
        return ResourceType(self)

    @cached_property
    def waitlist(self) -> Waitlist:
        """"""
        return Waitlist(self)
