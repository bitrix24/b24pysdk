import sys
from typing import Final, Tuple

MAX_BATCH_SIZE: Final[int] = 50
""""""

PYTHON_VERSION: Final[Tuple] = sys.version_info
""""""

TEXT_PYTHON_VERSION = f"{PYTHON_VERSION[0]}.{PYTHON_VERSION[1]}.{PYTHON_VERSION[2]}"
""""""
