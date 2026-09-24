import typing

from ..utils import enum as _enum

__all__ = [
    "EventType",
    "EventTypeLiteral",
]

EventTypeLiteral = typing.Literal["offline", "online"]


class EventType(_enum.StrEnum):
    """Supported Bitrix24 event delivery types."""
    OFFLINE = "offline"
    ONLINE = "online"
