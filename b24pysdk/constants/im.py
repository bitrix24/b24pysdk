from ..utils import enum as _enum

__all__ = [
    "ImChatColor",
    "ImChatEntityType",
    "ImChatType",
    "ImNotifyLastType",
]


class ImChatType(_enum.StrEnum):
    """Chat types for im.chat.add TYPE."""
    OPEN = "OPEN"
    CHAT = "CHAT"


class ImChatColor(_enum.StrEnum):
    """Chat colors for im.chat.add/updateColor COLOR."""
    RED = "RED"
    GREEN = "GREEN"
    MINT = "MINT"
    LIGHT_BLUE = "LIGHT_BLUE"
    DARK_BLUE = "DARK_BLUE"
    PURPLE = "PURPLE"
    AQUA = "AQUA"
    PINK = "PINK"
    LIME = "LIME"
    BROWN = "BROWN"
    AZURE = "AZURE"
    KHAKI = "KHAKI"
    SAND = "SAND"
    MARENGO = "MARENGO"
    GRAY = "GRAY"
    GRAPHITE = "GRAPHITE"


class ImChatEntityType(_enum.StrEnum):
    """Entity types for im.chat.add ENTITY_TYPE."""
    VIDEOCONF = "VIDEOCONF"
    AI_ASSISTANT_PRIVATE = "AI_ASSISTANT_PRIVATE"
    LINES = "LINES"
    LIVECHAT = "LIVECHAT"
    ANNOUNCEMENT = "ANNOUNCEMENT"
    CALENDAR = "CALENDAR"
    MAIL = "MAIL"
    CRM = "CRM"
    SONET_GROUP = "SONET_GROUP"
    TASKS = "TASKS"
    CALL = "CALL"


class ImNotifyLastType(_enum.IntEnum):
    """Pagination type values for im.notify.get LAST_TYPE."""
    CONFIRM = 1
    NOTIFICATION = 3
