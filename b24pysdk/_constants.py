import sys
from typing import Final, Tuple

from .utils.types import DefaultTimeout, Number

PYTHON_VERSION: Final[Tuple] = sys.version_info
""""""

TEXT_PYTHON_VERSION = f"{PYTHON_VERSION[0]}.{PYTHON_VERSION[1]}"
""""""

DEFAULT_TIMEOUT: Final[DefaultTimeout] = 10
""""""

INITIAL_RETRY_DELAY: Final[Number] = 1
""""""

MAX_BATCH_SIZE: Final[int] = 50
""""""

MAX_RETRIES: Final[int] = 3
""""""

RETRY_DELAY_INCREMENT: Final[Number] = 0
""""""
