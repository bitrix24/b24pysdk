from dataclasses import dataclass

from ..utils.dataclasses import frozen_dataclass_kwargs
from ._unbind_schema import UnbindData, UnbindSchema

__all__ = [
    "PlacementUnbind",
    "PlacementUnbindData",
]


PlacementUnbindData = UnbindData


@dataclass(**frozen_dataclass_kwargs())
class PlacementUnbind(UnbindSchema[PlacementUnbindData]):
    """
    Result returned by the ``placement.unbind`` method.

    The method removes registered placement handlers and returns the resulting
    operation count.
    """
