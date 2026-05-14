"""
Package version information.

This module contains metadata describing the installed SDK package.
The values defined here are intended for internal use and for exposing
version information via the public API.
"""

from typing import Final, Text

__all__ = [
    "__title__",
    "__version__",
]

__title__: Final[Text] = "b24pysdk"
"""Package name used for distribution and identification."""

__version__: Final[Text] = "1.1.0"
"""Current SDK version following semantic versioning."""
