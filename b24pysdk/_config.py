"""
SDK runtime configuration.

This module provides thread-local runtime configuration used to control
the behavior of the Bitrix SDK. Configuration options include:

- retry strategy
- request timeouts
- logging
- sensitive data masking
- timezone handling
- API version detection

The module also provides a process-wide registry that maps SDK object keys
and optional discriminators to Python object classes.

Each thread maintains its own configuration instance, allowing different
threads to use different SDK settings without interfering with each other.
"""

import threading
import typing
from datetime import date, datetime, timezone, tzinfo

from .constants import (
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_INITIAL_RETRY_DELAY,
    DEFAULT_MAX_RETRIES,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_RETRY_DELAY_INCREMENT,
)
from .constants.version import API_V3_METHODS
from .log import AbstractLogger, NullLogger
from .utils.types import DefaultTimeout, Number, ObjectDiscriminator, Timeout

if typing.TYPE_CHECKING:
    from .client import ClientType
    from .objects._base_object import BaseObject

__all__ = [
    "Config",
]

_TIMEOUT_TUPLE_LENGTH: typing.Final[int] = 2


class _LocalConfig:
    """
    Internal container for thread-local SDK configuration.

    Instances of this class store runtime configuration parameters
    used by the SDK. A separate instance is created for each thread
    via ``threading.local`` in the :class:`Config` class.
    """

    __slots__ = (
        "api_v3_methods",
        "default_client_factory",
        "default_connect_timeout",
        "default_initial_retry_delay",
        "default_max_retries",
        "default_read_timeout",
        "default_retry_delay_increment",
        "logger",
        "secure_log",
        "tz",
    )

    api_v3_methods: typing.Set[typing.Text]
    default_client_factory: typing.Optional[typing.Callable[[], "ClientType"]]
    default_connect_timeout: typing.Optional[Number]
    default_read_timeout: Number
    default_initial_retry_delay: Number
    default_max_retries: int
    default_retry_delay_increment: Number
    logger: AbstractLogger
    secure_log: bool
    tz: tzinfo

    def __init__(self):
        self.api_v3_methods = API_V3_METHODS
        self.default_client_factory = None
        self.default_connect_timeout = DEFAULT_CONNECT_TIMEOUT
        self.default_read_timeout = DEFAULT_READ_TIMEOUT
        self.default_initial_retry_delay = DEFAULT_INITIAL_RETRY_DELAY
        self.default_max_retries = DEFAULT_MAX_RETRIES
        self.default_retry_delay_increment = DEFAULT_RETRY_DELAY_INCREMENT
        self.logger = NullLogger()
        self.secure_log = True
        self.tz = self.__get_default_tz()

    def __get_default_tz(self) -> tzinfo:
        """
        Detect the system timezone.

        Attempts to determine the local system timezone using
        ``datetime.now().astimezone()``. If timezone detection fails,
        UTC is used as a fallback.

        Returns
        -------
        tzinfo
            Detected system timezone or ``timezone.utc`` if detection fails.
        """
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
    """
    Thread-local SDK configuration manager.

    This class provides access to runtime configuration settings used
    by the SDK, such as timeouts, retry policies, logging, and timezone
    handling.

    Each thread receives its own runtime configuration instance to avoid
    cross-thread interference. Object class registrations are process-wide
    because they describe imported Python classes rather than runtime settings.
    """

    __slots__ = ("_config",)

    _config: _LocalConfig

    _local_thread: threading.local = threading.local()
    _object_classes: typing.ClassVar[
        typing.Dict[
            typing.Tuple[typing.Text, ObjectDiscriminator],
            typing.Type["BaseObject"],
        ]
    ] = {}

    def __init__(self):
        local_thread = type(self)._local_thread

        if not hasattr(local_thread, "config"):
            local_thread.config = _LocalConfig()

        self._config = local_thread.config

    def configure(  # noqa: C901
            self,
            *,
            api_v3_methods: typing.Optional[typing.Iterable[typing.Text]] = None,
            default_client_factory: typing.Optional[typing.Callable[[], "ClientType"]] = None,
            default_initial_retry_delay: typing.Optional[Number] = None,
            default_max_retries: typing.Optional[int] = None,
            default_retry_delay_increment: typing.Optional[Number] = None,
            default_connect_timeout: typing.Optional[Number] = None,
            default_read_timeout: typing.Optional[Number] = None,
            default_timeout: Timeout = None,
            logger: typing.Optional[AbstractLogger] = None,
            log_level: typing.Optional[int] = None,
            secure_log: typing.Optional[bool] = None,
            tz: typing.Optional[tzinfo] = None,
    ):
        """
        Update SDK configuration values.

        Only parameters explicitly provided will be updated; all others
        remain unchanged.

        Parameters
        ----------
        api_v3_methods : Iterable[str], optional
            Collection of API method names that should be treated as Bitrix API v3 methods.

        default_client_factory : Callable[[], ClientType], optional
            Default factory used by the object layer when no explicit client or
            client_factory is passed. Configure it only for applications that
            work with a single Bitrix24 portal. Multi-portal applications should
            pass an explicit client or client_factory for each object operation.

        default_initial_retry_delay : Number, optional
            Initial delay (in seconds) before the first retry attempt.

        default_max_retries : int, optional
            Maximum number of retry attempts for failed requests.

        default_retry_delay_increment : Number, optional
            Increment added to retry delay after each retry.

        default_connect_timeout : Number, optional
            Default connection timeout in seconds.

        default_read_timeout : Number, optional
            Default read timeout in seconds.

        default_timeout : Timeout, optional
            Default timeout value for API calls. Can be a single number or
            a tuple of ``(connect_timeout, read_timeout)``.

        logger : AbstractLogger, optional
            Custom logger instance used by the SDK.

        log_level : int, optional
            Logging level to apply to the current logger.

        secure_log : bool, optional
            Whether SDK logs should hide credentials and other sensitive values.

        tz : tzinfo, optional
            Default timezone used by SDK date/time helpers.
        """

        if api_v3_methods is not None:
            self.api_v3_methods = api_v3_methods

        if default_client_factory is not None:
            self.default_client_factory = default_client_factory

        if default_initial_retry_delay is not None:
            self.default_initial_retry_delay = default_initial_retry_delay

        if default_max_retries is not None:
            self.default_max_retries = default_max_retries

        if default_retry_delay_increment is not None:
            self.default_retry_delay_increment = default_retry_delay_increment

        if default_connect_timeout is not None:
            self.default_connect_timeout = default_connect_timeout

        if default_read_timeout is not None:
            self.default_read_timeout = default_read_timeout

        if default_timeout is not None:
            self.default_timeout = default_timeout

        if logger is not None:
            self.logger = logger

        if log_level is not None:
            self.log_level = log_level

        if secure_log is not None:
            self.secure_log = secure_log

        if tz is not None:
            self.tz = tz

    @property
    def default_client_factory(self) -> typing.Optional[typing.Callable[[], "ClientType"]]:
        """Return the default object-layer client factory.

        Configure this setting only when the application works with a single
        Bitrix24 portal. Multi-portal applications should supply an explicit
        client or client_factory for each object operation instead.
        """
        return self._config.default_client_factory

    @default_client_factory.setter
    def default_client_factory(self, value: typing.Optional[typing.Callable[[], "ClientType"]]):
        """Set the default object-layer client factory.

        Configure this setting only when the application works with a single
        Bitrix24 portal. For multi-portal applications, keep it unset and pass an
        explicit client or client_factory for each object operation.
        """

        if value is not None and not callable(value):
            raise TypeError("default_client_factory must be callable or None")

        self._config.default_client_factory = value

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
    def default_connect_timeout(self) -> typing.Optional[Number]:
        """Connection timeout in seconds (None to use only read timeout)"""
        return self._config.default_connect_timeout

    @default_connect_timeout.setter
    def default_connect_timeout(self, value: typing.Optional[Number]):
        """Set connection timeout"""
        if value is not None and not (isinstance(value, (int, float)) and value > 0):
            raise ValueError("Connection timeout must be a positive number or None")
        self._config.default_connect_timeout = value

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
        """
        Default timeout used for API requests.

        The timeout value follows the same semantics as the ``timeout`` argument
        in the ``requests`` library.

        Returns
        -------
        DefaultTimeout
            One of the following values:

            - ``(connect_timeout, read_timeout)`` — if a separate connection
              timeout is configured.
            - ``read_timeout`` — if only a read timeout is configured.

        Notes
        -----
        If ``default_connect_timeout`` is ``None``, only the read timeout
        is applied to requests.
        """

        if self._config.default_connect_timeout is not None:
            return self._config.default_connect_timeout, self._config.default_read_timeout

        return self._config.default_read_timeout

    @default_timeout.setter
    def default_timeout(self, value: DefaultTimeout):
        """
        Set the default timeout for API requests.

        Parameters
        ----------
        value : DefaultTimeout
            Timeout configuration. Can be one of:

            - ``float`` or ``int`` — sets the read timeout only.
            - ``(connect_timeout, read_timeout)`` — sets both timeouts.

        Raises
        ------
        ValueError
            If timeout values are non-positive or invalid.

        TypeError
            If the value is not a number or a tuple of two numbers.

        Notes
        -----
        This method follows the same timeout semantics as the ``requests`` library.
        ``connect_timeout`` may be ``None`` to disable a separate connection timeout.
        """

        if isinstance(value, (int, float)):
            if value <= 0:
                raise ValueError("Timeout must be a positive number")

            self._config.default_connect_timeout = None
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

            self._config.default_connect_timeout = connect_timeout
            self._config.default_read_timeout = read_timeout

        else:
            raise TypeError(
                "Timeout must be a positive number or a tuple of (connect_timeout, read_timeout)",
            )

    @property
    def logger(self) -> AbstractLogger:
        """Current SDK logger instance."""
        return self._config.logger

    @logger.setter
    def logger(self, value: AbstractLogger):
        """
        Set the logger used by the SDK.

        Parameters
        ----------
        value : AbstractLogger
            Logger instance implementing the SDK logging interface.
        """

        if not isinstance(value, AbstractLogger):
            raise TypeError("Logger must be an instance of AbstractLogger")

        self._config.logger = value

    @property
    def log_level(self) -> int:
        """Current logging level of the SDK logger."""
        return self._config.logger.level

    @log_level.setter
    def log_level(self, value: int):
        """
        Set the logging level for the current logger.

        The value must be one of the levels defined in the logger's
        ``LOG_LEVELS`` mapping.
        """

        logger_class = self.logger.__class__

        if value not in logger_class.LOG_LEVELS.values():
            raise ValueError(
                f"Invalid log level: {value}. "
                f"It must be one of the levels defined in {logger_class.__name__}.LOG_LEVELS: "
                f"{', '.join(map(str, logger_class.LOG_LEVELS.values()))}",
            )

        self._config.logger.set_level(value)

    @property
    def secure_log(self) -> bool:
        """Whether SDK logs should hide credentials and other sensitive values."""
        return self._config.secure_log

    @secure_log.setter
    def secure_log(self, value: bool):
        """Set secure logging mode for SDK logs."""

        if not isinstance(value, bool):
            raise TypeError("secure_log must be a boolean")

        self._config.secure_log = value

    @property
    def tz(self) -> tzinfo:
        """
        Default timezone used by the SDK.

        This timezone is applied by helper methods such as
        :meth:`get_local_datetime` and :meth:`get_local_date`.
        """
        return self._config.tz

    @tz.setter
    def tz(self, value: tzinfo):
        """Set the default timezone used by the SDK."""

        if not isinstance(value, tzinfo):
            raise TypeError("tzinfo must be an instance of datetime.tzinfo")

        self._config.tz = value

    @property
    def api_v3_methods(self) -> typing.Set[typing.Text]:
        """Set of API method names that should be treated as Bitrix API v3 methods."""
        return self._config.api_v3_methods

    @api_v3_methods.setter
    def api_v3_methods(self, value: typing.Iterable[typing.Text]):
        """
        Set the collection of API methods that use Bitrix REST API v3.

        Parameters
        ----------
        value : Iterable[Text]
            Iterable of method names. A plain string is not accepted because
            it would otherwise be interpreted as an iterable of characters.
        """

        if isinstance(value, (str, bytes)) or not isinstance(value, typing.Iterable):
            raise TypeError("api_v3_methods must be an iterable of strings, not a string")

        api_v3_methods = set(value)

        if not all(isinstance(api_v3_method, str) for api_v3_method in api_v3_methods):
            raise TypeError("All api_v3_methods entries must be strings")

        self._config.api_v3_methods = api_v3_methods

    def is_api_v3_method(self, api_method: typing.Text) -> bool:
        """
        Check whether the specified API method belongs to Bitrix REST API v3.

        Parameters
        ----------
        api_method : Text
            Name of the API method.

        Returns
        -------
        bool
            True if the method is configured as an API v3 method.
        """
        return api_method in self.api_v3_methods

    def get_local_date(
            self,
            *,
            dt: typing.Optional[datetime] = None,
            tz: typing.Optional[tzinfo] = None,
    ) -> date:
        """
        Return the local date according to the configured timezone.

        Parameters
        ----------
        dt : datetime, optional
            Datetime to convert to the configured timezone.
            If omitted, the current time is used.

        tz : tzinfo, optional
            Timezone override.

        Returns
        -------
        date
            Local date in the resolved timezone.
        """
        return self.get_local_datetime(dt=dt, tz=tz).date()

    def get_local_datetime(
            self,
            *,
            dt: typing.Optional[datetime] = None,
            tz: typing.Optional[tzinfo] = None,
    ) -> datetime:
        """
        Return a datetime adjusted to the configured timezone.

        Parameters
        ----------
        dt : datetime, optional
            Datetime to convert to the target timezone.
            If omitted, the current time is used.

        tz : tzinfo, optional
            Timezone override. If not provided, the configured SDK
            timezone is used.

        Returns
        -------
        datetime
            Datetime object adjusted to the resolved timezone.
        """

        if tz is None:
            tz = self.tz

        if dt is None:
            dt = datetime.now(tz=tz)
        else:
            dt = dt.astimezone(tz=tz)

        return dt

    @classmethod
    def register_object_class(
            cls,
            *,
            object_key: typing.Text,
            discriminator: ObjectDiscriminator,
            object_class: typing.Type["BaseObject"],
    ):
        """
        Register a Python object class for an SDK object key.

        A registration is identified by the pair ``(object_key, discriminator)``.
        Registering the same pair again replaces the previously registered class,
        provided that the new class inherits from the currently registered class.

        When registering a discriminator-specific class for the first time, the
        default ``(object_key, None)`` class is used as the required base class.

        Parameters
        ----------
        object_key : Text
            Stable SDK object key, for example ``"department"`` or ``"crm.item"``.

        object_class : type
            Python class used to represent the object.

        discriminator : ObjectDiscriminator
            Hashable entity discriminator. Tuple discriminators are resolved
            from the most specific value to progressively broader defaults.

        Raises
        ------
        TypeError
            If ``object_class`` does not inherit from the
            previously registered class for the same entity.
        """

        registry_key = object_key, discriminator
        registered_class = cls._object_classes.get(registry_key)

        if registered_class is None:
            candidates = cls._get_discriminator_candidates(discriminator)
            next(candidates)

            for candidate in candidates:
                registered_class = cls._object_classes.get((object_key, candidate))

                if registered_class is not None:
                    break

        if registered_class is not None and not issubclass(object_class, registered_class):
            raise TypeError(
                f"{object_class.__name__} must inherit from "
                f"{registered_class.__name__} for object_key={object_key!r}, "
                f"discriminator={discriminator!r}",
            )

        cls._object_classes[registry_key] = object_class

    @classmethod
    def get_object_class(
            cls,
            *,
            object_key: typing.Text,
            discriminator: ObjectDiscriminator = None,
    ) -> typing.Type["BaseObject"]:
        """
        Return the registered Python class for an SDK object key.

        The exact ``(object_key, discriminator)`` registration is preferred.
        Tuple discriminators fall back from right to left by replacing values
        with ``None``. The default ``(object_key, None)`` registration is tried
        last.

        Raises
        ------
        KeyError
            If neither an exact nor a default registration exists.
        """

        for candidate in cls._get_discriminator_candidates(discriminator):
            object_class = cls._object_classes.get((object_key, candidate))

            if object_class is not None:
                return object_class

        raise KeyError(
            f"No object class registered for object_key={object_key!r}, "
            f"discriminator={discriminator!r}.",
        )

    @classmethod
    def _get_discriminator_candidates(cls, discriminator: ObjectDiscriminator) -> typing.Iterator[ObjectDiscriminator]:
        """Yield discriminator candidates from the most specific to the default."""

        try:
            hash(discriminator)
        except TypeError:
            raise TypeError("Object class discriminator must be hashable.") from None

        yield discriminator

        if isinstance(discriminator, tuple):
            candidate = list(discriminator)

            for index in range(len(candidate) - 1, -1, -1):
                if candidate[index] is None:
                    continue

                candidate[index] = None
                yield tuple(candidate)

            yield None

        elif discriminator is not None:
            yield None
