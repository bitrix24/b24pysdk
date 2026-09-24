from ..utils import enum as _enum

__all__ = [
    "TaskCounterType",
    "TaskStagesEntityType",
]


class TaskCounterType(_enum.StrEnum):
    """Counter roles for tasks.task.counters.get type."""
    VIEW_ALL = "view_all"
    VIEW_ROLE_RESPONSIBLE = "view_role_responsible"
    VIEW_ROLE_ACCOMPLICE = "view_role_accomplice"
    VIEW_ROLE_AUDITOR = "view_role_auditor"
    VIEW_ROLE_ORIGINATOR = "view_role_originator"


class TaskStagesEntityType(_enum.StrEnum):
    """Entity types for task.stages.canmovetask entityType."""
    USER = "U"
    GROUP = "G"
