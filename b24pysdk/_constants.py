import sys
from typing import Final, Text, Tuple

__all__ = [
    "MAX_BATCH_SIZE",
    "PYTHON_VERSION",
    "TEXT_PYTHON_VERSION",
]

MAX_BATCH_SIZE: Final[int] = 50
""""""

PYTHON_VERSION: Final[Tuple] = sys.version_info
""""""

TEXT_PYTHON_VERSION: Final[Text] = f"{PYTHON_VERSION[0]}.{PYTHON_VERSION[1]}.{PYTHON_VERSION[2]}"
""""""
