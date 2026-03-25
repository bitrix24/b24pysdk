from ..utils import enum as _enum

__all__ = [
    "TimecontrolReportType",
]


class TimecontrolReportType(_enum.StrEnum):
    """Access types for timeman.timecontrol.settings.set report params."""
    ALL = "all"
    USER = "user"
    NONE = "none"
