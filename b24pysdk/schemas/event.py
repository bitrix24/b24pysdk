from dataclasses import dataclass

from ..utils.dataclasses import frozen_dataclass_kwargs
from ._unbind_schema import UnbindData, UnbindSchema

__all__ = [
    "EventUnbind",
    "EventUnbindData",
]


EventUnbindData = UnbindData


@dataclass(**frozen_dataclass_kwargs())
class EventUnbind(UnbindSchema[EventUnbindData]):
    """
    Result returned by the ``event.unbind`` method.

    The method removes registered event handlers and returns the resulting
    operation count.
    """
