from ..utils import enum as _enum

__all__ = [
    "RpaFieldVisibility",
    "RpaStageSemantic",
]


class RpaStageSemantic(_enum.StrEnum):
    """Stage semantic codes for rpa.stage.add/update."""
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


class RpaFieldVisibility(_enum.StrEnum):
    """Visibility identifiers for rpa.fields.setVisibilitySettings."""
    KANBAN = "kanban"
