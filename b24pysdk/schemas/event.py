from typing import Optional, Text, TypedDict

from ..utils.types import JSONList

__all__ = [
    "EventOfflineGetData",
]


class EventOfflineGetData(TypedDict):
    """Raw result returned by ``event.offline.get``."""
    process_id: Optional[Text]
    events: JSONList
