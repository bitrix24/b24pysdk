from ..utils import enum as _enum

__all__ = [
    "EngineCategory",
    "PromptSection",
]


class EngineCategory(_enum.StrEnum):
    """AI engine categories."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"


class PromptSection(_enum.StrEnum):
    """AI prompt sections."""
    CREATE = "create"
    EDIT = "edit"
