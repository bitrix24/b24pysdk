"""
Public SDK version information.

This module exposes the SDK name and version intended for external use.
Unlike `_version`, which stores internal package metadata, this module
provides stable constants that can be safely imported by SDK users.
"""

from typing import Final, Text

from ._version import __title__, __version__

__all__ = [
    "SDK_NAME",
    "SDK_VERSION",
]

SDK_NAME: Final[Text] = __title__
"""Name of the SDK package."""

SDK_VERSION: Final[Text] = __version__
"""Current SDK version following semantic versioning."""
