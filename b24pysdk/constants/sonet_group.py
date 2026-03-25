from ..utils import enum as _enum

__all__ = [
    "SonetGroupMemberRole",
    "SonetGroupPermissionRole",
]


class SonetGroupMemberRole(_enum.StrEnum):
    """Group member roles."""
    OWNER = "A"
    MODERATOR = "E"
    MEMBER = "K"


class SonetGroupPermissionRole(_enum.StrEnum):
    """Role codes used by INITIATE_PERMS / SPAM_PERMS."""
    OWNER_ONLY = "A"
    OWNER_AND_MODERATORS = "E"
    ALL_MEMBERS = "K"
