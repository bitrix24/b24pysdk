from typing import Final, Text

from ._version import __title__, __version__

__all__ = [
    "SDK_NAME",
    "SDK_VERSION",
]

SDK_NAME: Final[Text] = __title__
SDK_VERSION: Final[Text] = __version__
