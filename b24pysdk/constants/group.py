import typing

from ..utils import enum as _enum

__all__ = [
    "GroupAvatarType",
    "GroupAvatarTypeLiteral",
    "GroupMemberRole",
    "GroupPermissionRole",
    "GroupPermissionRoleLiteral",
    "GroupPrivacy",
    "GroupPrivacyLiteral",
    "GroupScrumTaskResponsible",
    "GroupScrumTaskResponsibleLiteral",
    "GroupType",
    "GroupTypeLiteral",
]


GroupAvatarTypeLiteral = typing.Literal["folder", "checks", "pie", "bag", "members"]
"""Literal type for Bitrix24 group system avatars."""


class GroupAvatarType(_enum.StrEnum):
    """System avatar type assigned to a Bitrix24 group."""
    FOLDER = "folder"
    CHECKS = "checks"
    PIE = "pie"
    BAG = "bag"
    MEMBERS = "members"


GroupPermissionRoleLiteral = typing.Literal["A", "E", "K"]


class GroupPermissionRole(_enum.StrEnum):
    OWNER_ONLY = "A"
    OWNER_AND_MODERATORS = "E"
    ALL_MEMBERS = "K"


class GroupMemberRole(_enum.StrEnum):
    """Group member roles."""
    OWNER = "A"
    MODERATOR = "E"
    MEMBER = "K"


GroupScrumTaskResponsibleLiteral = typing.Literal["A", "M"]
"""Literal type for the default responsible user for scrum tasks."""


class GroupScrumTaskResponsible(_enum.StrEnum):
    """Default responsible user for newly created scrum tasks."""
    TASK_CREATOR = "A"
    SCRUM_MASTER = "M"


GroupTypeLiteral = typing.Literal["group", "project", "scrum", "collab"]
"""Literal type for Bitrix24 group types."""


class GroupType(_enum.StrEnum):
    """Bitrix24 group type."""
    GROUP = "group"
    PROJECT = "project"
    SCRUM = "scrum"
    COLLAB = "collab"


GroupPrivacyLiteral = typing.Literal["open", "closed", "secret"]
"""Literal type for Bitrix24 group privacy levels."""


class GroupPrivacy(_enum.StrEnum):
    """Bitrix24 group privacy level."""
    OPEN = "open"
    CLOSED = "closed"
    SECRET = "secret"  # noqa: S105
