import threading

from ._constants import DEFAULT_TIMEOUT, INITIAL_RETRY_DELAY, MAX_RETRIES, RETRY_DELAY_INCREMENT
from .log import AbstractLogger, NullLogger
from .utils.types import DefaultTimeout, Number


class _LocalConfig:
    """"""

    __slots__ = (
        "default_timeout",
        "initial_retry_delay",
        "logger",
        "max_retries",
        "retry_delay_increment",
    )

    default_timeout: DefaultTimeout
    initial_retry_delay: Number
    logger: AbstractLogger
    max_retries: int
    retry_delay_increment: Number

    def __init__(self):
        self.default_timeout: DefaultTimeout = DEFAULT_TIMEOUT
        self.initial_retry_delay: Number = INITIAL_RETRY_DELAY
        self.logger = NullLogger()
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
    def logger(self) -> AbstractLogger:
        """"""
        return self._config.logger

    @logger.setter
    def logger(self, value: AbstractLogger):
        """"""

        if not isinstance(value, AbstractLogger):
            raise TypeError("Logger must be an instance of AbstractLogger")

        self._config.logger = value

    @property
    def log_level(self) -> int:
        """"""
        return self._config.logger.level

    @log_level.setter
    def log_level(self, value: int):
        """"""

        logger_class = self.logger.__class__

        if value not in logger_class.LOG_LEVELS.values():
            raise ValueError(
                f"Invalid log level: {value}. "
                f"It must be one of the levels defined in {logger_class.__name__}.LOG_LEVELS: "
                f"{', '.join(map(str, logger_class.LOG_LEVELS.values()))}",
            )

        self._config.logger.set_level(value)

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
