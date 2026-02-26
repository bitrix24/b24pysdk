import threading
import typing
from datetime import date, datetime, timezone, tzinfo

from .constants import DEFAULT_CONNECTION_TIMEOUT, DEFAULT_INITIAL_RETRY_DELAY, DEFAULT_MAX_RETRIES, DEFAULT_READ_TIMEOUT, DEFAULT_RETRY_DELAY_INCREMENT
from .constants.version import API_V3_METHODS
from .log import AbstractLogger, NullLogger
from .utils.types import DefaultTimeout, Number, Timeout

__all__ = [
    "Config",
]

_TIMEOUT_TUPLE_LENGTH: typing.Final[int] = 2


class _LocalConfig:
    """"""

    __slots__ = (
        "api_v3_methods",
        "default_connection_timeout",
        "default_initial_retry_delay",
        "default_max_retries",
        "default_read_timeout",
        "default_retry_delay_increment",
        "logger",
        "tz",
    )

    api_v3_methods: typing.Tuple[typing.Text, ...]
    default_connection_timeout: typing.Optional[Number]
    default_read_timeout: Number
    default_initial_retry_delay: Number
    default_max_retries: int
    default_retry_delay_increment: Number
    logger: AbstractLogger
    tz: tzinfo

    def __init__(self):
        self.api_v3_methods = API_V3_METHODS
        self.default_connection_timeout = DEFAULT_CONNECTION_TIMEOUT
        self.default_read_timeout = DEFAULT_READ_TIMEOUT
        self.default_initial_retry_delay = DEFAULT_INITIAL_RETRY_DELAY
        self.default_max_retries = DEFAULT_MAX_RETRIES
        self.default_retry_delay_increment = DEFAULT_RETRY_DELAY_INCREMENT
        self.logger = NullLogger()
        self.tz = self.__get_default_tz()

    def __get_default_tz(self) -> tzinfo:
        try:
            tz = datetime.now().astimezone().tzinfo
        except OSError as error:
            self.logger.warning(
                "Failed to detect system tzinfo, falling back to UTC",
                context={
                    "error": error,
                },
            )
            tz = timezone.utc
        else:
            if tz is None:
                self.logger.warning("Failed to detect system tzinfo, falling back to UTC")
                tz = timezone.utc
        return tz


class Config:
    """Thread-local configuration for SDK behavior"""

    __slots__ = ("_config",)

    _config: _LocalConfig

    _local_thread: threading.local = threading.local()

    def __init__(self):
        local_thread = type(self)._local_thread

        if not hasattr(local_thread, "config"):
            local_thread.config = _LocalConfig()

        self._config = local_thread.config

    def configure(  # noqa: C901
            self,
            *,
            api_v3_methods: typing.Optional[typing.Iterable[typing.Text]] = None,
            default_initial_retry_delay: typing.Optional[Number] = None,
            default_max_retries: typing.Optional[int] = None,
            default_retry_delay_increment: typing.Optional[Number] = None,
            default_connection_timeout: typing.Optional[Number] = None,
            default_read_timeout: typing.Optional[Number] = None,
            default_timeout: Timeout = None,
            logger: typing.Optional[AbstractLogger] = None,
            log_level: typing.Optional[int] = None,
            tz: typing.Optional[tzinfo] = None,
    ):
        """"""

        if api_v3_methods is not None:
            self.api_v3_methods = api_v3_methods if isinstance(api_v3_methods, tuple) else tuple(api_v3_methods)

        if default_initial_retry_delay is not None:
            self.default_initial_retry_delay = default_initial_retry_delay

        if default_max_retries is not None:
            self.default_max_retries = default_max_retries

        if default_retry_delay_increment is not None:
            self.default_retry_delay_increment = default_retry_delay_increment

        if default_connection_timeout is not None:
            self.default_connection_timeout = default_connection_timeout

        if default_read_timeout is not None:
            self.default_read_timeout = default_read_timeout

        if default_timeout is not None:
            self.default_timeout = default_timeout

        if logger is not None:
            self.logger = logger

        if log_level is not None:
            self.log_level = log_level

        if tz is not None:
            self.tz = tz

    @property
    def default_initial_retry_delay(self) -> Number:
        """Initial delay between retries in seconds"""
        return self._config.default_initial_retry_delay

    @default_initial_retry_delay.setter
    def default_initial_retry_delay(self, value: Number):
        """"""
        if not (isinstance(value, (int, float)) and value > 0):
            raise ValueError("Initial_retry_delay must be a positive number")
        self._config.default_initial_retry_delay = value

    @property
    def default_max_retries(self) -> int:
        """Maximum number retries that will occur when server is not responding"""
        return self._config.default_max_retries

    @default_max_retries.setter
    def default_max_retries(self, value: int):
        """"""
        if not (isinstance(value, int) and value >= 1):
            raise ValueError("Max_retries must be a positive integer (>= 1)")
        self._config.default_max_retries = value

    @property
    def default_retry_delay_increment(self) -> Number:
        """Amount by which delay between retries will increment after each retry"""
        return self._config.default_retry_delay_increment

    @default_retry_delay_increment.setter
    def default_retry_delay_increment(self, value: Number):
        """"""
        if not (isinstance(value, (int, float)) and value >= 0):
            raise ValueError("Retry_delay_increment must be a positive number")
        self._config.default_retry_delay_increment = value

    @property
    def default_connection_timeout(self) -> typing.Optional[Number]:
        """Connection timeout in seconds (None to use only read timeout)"""
        return self._config.default_connection_timeout

    @default_connection_timeout.setter
    def default_connection_timeout(self, value: typing.Optional[Number]):
        """Set connection timeout"""
        if value is not None and not (isinstance(value, (int, float)) and value > 0):
            raise ValueError("Connection timeout must be a positive number or None")
        self._config.default_connection_timeout = value

    @property
    def default_read_timeout(self) -> Number:
        """Read timeout in seconds"""
        return self._config.default_read_timeout

    @default_read_timeout.setter
    def default_read_timeout(self, value: Number):
        """Set read timeout"""
        if not (isinstance(value, (int, float)) and value > 0):
            raise ValueError("Read timeout must be a positive number")
        self._config.default_read_timeout = value

    @property
    def default_timeout(self) -> DefaultTimeout:
        """Default timeout for API calls.

        Returns:
            - (connection_timeout, read_timeout) if connection_timeout is set
            - read_timeout if connection_timeout is None
        """
        if self._config.default_connection_timeout is not None:
            return self._config.default_connection_timeout, self._config.default_read_timeout
        return self._config.default_read_timeout

    @default_timeout.setter
    def default_timeout(self, value: DefaultTimeout):
        """Set timeout (can be a number or tuple)"""

        if isinstance(value, (int, float)):
            if value <= 0:
                raise ValueError("Timeout must be a positive number")

            self._config.default_connection_timeout = None
            self._config.default_read_timeout = value

        elif isinstance(value, tuple):
            if len(value) != _TIMEOUT_TUPLE_LENGTH:
                raise ValueError(
                    "Timeout tuple must contain exactly two values: "
                    "(connect_timeout, read_timeout)",
                )

            connect_timeout, read_timeout = value

            if connect_timeout is not None and not (isinstance(connect_timeout, (int, float)) and connect_timeout > 0):
                raise ValueError("Connection timeout must be a positive number or None")

            if not (isinstance(read_timeout, (int, float)) and read_timeout > 0):
                raise ValueError("Read timeout must be a positive number")

            self._config.default_connection_timeout = connect_timeout
            self._config.default_read_timeout = read_timeout

        else:
            raise TypeError(
                "Timeout must be a positive number or a tuple of (connect_timeout, read_timeout)",
            )

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
    def tz(self) -> tzinfo:
        """"""
        return self._config.tz

    @tz.setter
    def tz(self, value: tzinfo):
        """"""
        if not isinstance(value, tzinfo):
            raise TypeError("tzinfo must be an instance of datetime.tzinfo")
        self._config.tz = value

    @property
    def api_v3_methods(self) -> typing.Tuple[typing.Text, ...]:
        """"""
        return self._config.api_v3_methods

    @api_v3_methods.setter
    def api_v3_methods(self, value: typing.Iterable[typing.Text]):
        """"""

        if not isinstance(value, typing.Iterable):
            raise TypeError("api_v3_methods must be an iterable of strings")

        api_v3_methods = value if isinstance(value, tuple) else tuple(value)

        if not all(isinstance(api_v3_method, str) for api_v3_method in api_v3_methods):
            raise TypeError("All api_v3_methods entries must be strings")

        self._config.api_v3_methods = api_v3_methods

    def is_api_v3_method(self, api_method: typing.Text) -> bool:
        """"""
        return api_method in self.api_v3_methods

    def get_local_date(
            self,
            *,
            dt: typing.Optional[datetime] = None,
            tz: typing.Optional[tzinfo] = None,
    ) -> date:
        """"""
        return self.get_local_datetime(dt=dt, tz=tz).date()

    def get_local_datetime(
            self,
            *,
            dt: typing.Optional[datetime] = None,
            tz: typing.Optional[tzinfo] = None,
    ) -> datetime:
        """"""

        if tz is None:
            tz = self.tz

        if dt is None:
            dt = datetime.now(tz=tz)
        else:
            dt = dt.astimezone(tz=tz)

        return dt
