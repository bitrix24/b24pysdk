from ..utils import enum as _enum

__all__ = [
    "VoteAttachedEntityType",
    "VoteAttachedModule",
    "VoteQuestionFieldType",
]


class VoteAttachedModule(_enum.StrEnum):
    """Module IDs for attached votes."""
    IM = "Im"
    BLOG = "blog"


class VoteAttachedEntityType(_enum.StrEnum):
    """Entity connector types for attached votes."""
    IM_MESSAGE = "Bitrix\\Vote\\Attachment\\ImMessageConnector"
    BLOG_POST = "Bitrix\\Vote\\Attachment\\BlogPostConnector"


class VoteQuestionFieldType(_enum.IntEnum):
    """Answer field types for vote.Integration.Im.send."""
    SINGLE_CHOICE = 0
    MULTIPLE_CHOICE = 1
