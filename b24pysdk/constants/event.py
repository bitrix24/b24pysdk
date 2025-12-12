from ..utils import enum as _enum

__all__ = [
    "EventType",
]


class EventType(_enum.StrEnum):
    """"""
    OFFLINE = "offline"
    ONLINE = "online"
