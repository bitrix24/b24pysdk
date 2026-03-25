"""
Internal SDK constants.

This module defines commonly used constants shared across the SDK,
including API limits and runtime environment information.
"""

import sys
from typing import Final, Text, Tuple

__all__ = [
    "DEFAULT_REQUEST_ID_HEADER_NAME",
    "MAX_BATCH_SIZE",
    "PYTHON_VERSION",
    "SDK_USER_AGENT",
    "TEXT_PYTHON_VERSION",
]

DEFAULT_REQUEST_ID_HEADER_NAME: Final[Text] = "X-Request-ID"
"""
HTTP header name used to propagate request identifiers.

This header may be used for request tracing and debugging across
services interacting with the Bitrix API.
"""

MAX_BATCH_SIZE: Final[int] = 50
"""
Maximum number of commands allowed in a single Bitrix REST batch request.

According to the Bitrix API specification, a batch request may contain
up to 50 individual commands.
"""

PYTHON_VERSION: Final[Tuple] = sys.version_info
"""
Current Python runtime version.

This value is taken from ``sys.version_info`` and may be used for
diagnostics, logging, or constructing User-Agent headers.
"""

SDK_USER_AGENT: Final[Text] = "b24-python-sdk-vendor"
"""
Base User-Agent identifier used by the SDK.

This value represents the SDK vendor or implementation and is typically
combined with the SDK version and Python runtime information when
constructing the final HTTP User-Agent header.
"""

TEXT_PYTHON_VERSION: Final[Text] = f"{PYTHON_VERSION[0]}.{PYTHON_VERSION[1]}.{PYTHON_VERSION[2]}"
"""Human-readable Python version string."""
