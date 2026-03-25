from ..utils import enum as _enum

__all__ = [
    "BotColor",
    "BotType",
]


class BotType(_enum.StrEnum):
    """Bitrix24 IM bot types."""
    BOT = "B"
    OPENLINE = "O"
    HUMAN = "H"
    SUPPORT = "S"


class BotColor(_enum.StrEnum):
    """Available profile colors for imbot.register PROPERTIES.COLOR."""
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
