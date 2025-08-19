import sys
from typing import Final

from .utils.types import DefaultTimeout, Number

PYTHON_VERSION = sys.version_info

DEFAULT_TIMEOUT: Final[DefaultTimeout] = 10

INITIAL_RETRY_DELAY: Final[Number] = 1

MAX_BATCH_SIZE: Final[int] = 50

MAX_RETRIES: Final[int] = 3

RETRY_DELAY_INCREMENT: Final[Number] = 0
