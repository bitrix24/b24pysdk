import threading

from ._constants import DEFAULT_TIMEOUT, INITIAL_RETRY_DELAY, MAX_RETRIES, RETRY_DELAY_INCREMENT
from .utils.types import DefaultTimeout, Number


class _LocalConfig:
    """"""

    __slots__ = (
        "default_timeout",
        "initial_retry_delay",
        "max_retries",
        "retry_delay_increment",
    )

    initial_retry_delay: Number
    default_timeout: DefaultTimeout
    max_retries: int
    retry_delay_increment: Number

    def __init__(self):
        self.default_timeout: DefaultTimeout = DEFAULT_TIMEOUT
        self.initial_retry_delay: Number = INITIAL_RETRY_DELAY
        self.max_retries: int = MAX_RETRIES
        self.retry_delay_increment: Number = RETRY_DELAY_INCREMENT


class Config:
    """Thread-local configuration for SDK behavior"""

    _local_thread = threading.local()

    def __init__(self):
        local_thread = type(self)._local_thread

        if not hasattr(local_thread, "config"):
            local_thread.config = _LocalConfig()

        self._config = local_thread.config

    @property
    def default_timeout(self) -> DefaultTimeout:
        """Default timeout for API calls"""
        return self._config.default_timeout

    @default_timeout.setter
    def default_timeout(self, value: DefaultTimeout):
        """"""

        if not (isinstance(value, (int, float)) and value > 0):
            raise ValueError("Default_timeout must be a positive number or a tuple of two positive numbers (connect_timeout, read_timeout)")

        self._config.default_timeout = value

    @property
    def max_retries(self) -> int:
        """Maximum number retries that will occur when server is not responding"""
        return self._config.max_retries

    @max_retries.setter
    def max_retries(self, value: int):
        """"""

        if not (isinstance(value, int) and value >= 1):
            raise ValueError("Max_retries must be a positive integer (>= 1)")

        self._config.max_retries = value

    @property
    def initial_retry_delay(self) -> Number:
        """Initial delay between retries in seconds"""
        return self._config.initial_retry_delay

    @initial_retry_delay.setter
    def initial_retry_delay(self, value: Number):
        """"""

        if not (isinstance(value, (int, float)) and value > 0):
            raise ValueError("Initial_retry_delay must be a positive number")

        self._config.initial_retry_delay = value

    @property
    def retry_delay_increment(self) -> Number:
        """Amount by which delay between retries will increment after each retry"""
        return self._config.retry_delay_increment

    @retry_delay_increment.setter
    def retry_delay_increment(self, value: Number):
        """"""

        if not (isinstance(value, (int, float)) and value >= 0):
            raise ValueError("Retry_delay_increment must be a positive number")

        self._config.retry_delay_increment = value
