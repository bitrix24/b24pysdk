import os
import time
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Dict, Final, Optional, Text, Tuple

import requests

try:
    from uuid import uuid7
except ImportError:
    from uuid6 import uuid7

from ..._config import Config
from ..._constants import DEFAULT_REQUEST_ID_HEADER_NAME, MASKED_VALUE, SDK_USER_AGENT, TEXT_PYTHON_VERSION
from ...utils.types import DefaultTimeout, JSONDict, Number, Timeout
from ...version import SDK_VERSION
from ._utils import parse_response

__all__ = [
    "BaseRequester",
]


class BaseRequester(ABC):
    """
    Base class for Bitrix24 HTTP requesters.

    Provides shared configuration, default SDK headers, request ID generation,
    response parsing, and retry handling for concrete requester implementations.
    """

    _DEFAULT_REQUEST_ID_HEADER_NAME: Final[Text] = DEFAULT_REQUEST_ID_HEADER_NAME
    _SDK_VERSION: Final[Text] = SDK_VERSION
    _SDK_USER_AGENT: Final[Text] = SDK_USER_AGENT
    _TEXT_PYTHON_VERSION: Final[Text] = TEXT_PYTHON_VERSION
    _MASKED_VALUE: Final[Text] = MASKED_VALUE

    _KEY_NAME_VARIANTS: Final[Tuple[Text, ...]] = (
        "REQUEST_ID",
        "HTTP_X_REQUEST_ID",
        "UNIQUE_ID",
    )

    __slots__ = (
        "_config",
        "_initial_retry_delay",
        "_max_retries",
        "_retries_remaining",
        "_retry_delay_increment",
        "_timeout",
    )

    _config: Config
    _initial_retry_delay: Number
    _max_retries: int
    _retries_remaining: int
    _retry_delay_increment: Number
    _timeout: DefaultTimeout

    def __init__(
            self,
            *,
            timeout: Timeout = None,
            max_retries: Optional[int] = None,
            initial_retry_delay: Optional[Number] = None,
            retry_delay_increment: Optional[Number] = None,
    ):
        """
        Initialize requester configuration.

        Args:
            timeout: Request timeout. Falsy values fall back to the global SDK
                default timeout.
            max_retries: Maximum number of request attempts. Falsy values fall
                back to the global SDK default retry count.
            initial_retry_delay: Delay before the first retry. Falsy values fall
                back to the global SDK default initial retry delay.
            retry_delay_increment: Additional delay added after each used retry.
                Falsy values fall back to the global SDK default increment.
        """
        self._config = Config()
        self._timeout = timeout or self._config.default_timeout
        self._max_retries = max_retries or self._config.default_max_retries
        self._retries_remaining = self._max_retries
        self._initial_retry_delay = initial_retry_delay or self._config.default_initial_retry_delay
        self._retry_delay_increment = retry_delay_increment or self._config.default_retry_delay_increment

    @property
    @abstractmethod
    def _headers(self) -> Dict:
        """Return headers used for the concrete request type."""
        raise NotImplementedError

    def _get_default_headers(self) -> Dict[Text, Text]:
        """
        Build default SDK headers for outgoing requests.

        Returns:
            Headers containing JSON accept metadata, SDK version information,
            Python version information, user agent, and request ID.
        """
        return {
            "Accept": "application/json",
            "Accept-Charset": "utf-8",
            "User-Agent": f"{self._SDK_USER_AGENT}-v-{self._SDK_VERSION}-python-{self._TEXT_PYTHON_VERSION}",
            "X-BITRIX24-PYTHON-SDK-PYTHON-VERSION": self._TEXT_PYTHON_VERSION,
            "X-BITRIX24-PYTHON-SDK-VERSION": self._SDK_VERSION,
            self._DEFAULT_REQUEST_ID_HEADER_NAME: self.get_request_id(),
        }

    @abstractmethod
    def _request(self, *args, **kwargs) -> requests.Response:
        """Execute a single HTTP request without retry/error wrapping."""
        raise NotImplementedError

    @classmethod
    def _parse_response(cls, response: requests.Response) -> JSONDict:
        """
        Parse and validate a Bitrix24 HTTP response.

        Args:
            response: Raw HTTP response returned by ``requests``.

        Returns:
            Parsed JSON-compatible response dictionary.
        """
        return parse_response(response)

    @property
    def _used_retries(self) -> int:
        """Amount of retries already used."""
        return self._max_retries - self._retries_remaining

    @property
    def _retry_timeout(self) -> float:
        """
        Calculate delay before the next retry.

        Returns:
            Number of seconds to sleep before the next request attempt.
        """
        return self._initial_retry_delay + self._used_retries * self._retry_delay_increment

    def _request_with_retries(self, *args, **kwargs) -> requests.Response:
        """
        Execute request with retry handling for temporary service unavailability.

        Retries are performed only for HTTP 503 responses. Other responses are
        returned immediately and parsed by higher-level code.

        Returns:
            HTTP response from the last request attempt.

        Raises:
            RuntimeError: If all retry attempts are exhausted without receiving
                a response that should be returned to the caller.
        """

        self._retries_remaining = self._max_retries

        while self._retries_remaining > 0:

            self._retries_remaining -= 1
            response = self._request(*args, **kwargs)

            if self._retries_remaining and response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
                self._config.logger.warning(
                    "Service unavailable!",
                    context={
                        "URL": self._get_url_for_log(response.url),
                        "retry_count": self._used_retries,
                        "max_retries": self._max_retries,
                        "retries_remaining": self._retries_remaining,
                    },
                )
                self._config.logger.info(
                    "Sleep before retry",
                    context={
                        "sleep_time": self._retry_timeout,
                    },
                )
                time.sleep(self._retry_timeout)
                continue

            return response

        raise RuntimeError(
            f"Request failed after {self._max_retries} attempts. "
            "No valid response was received from the server.",
        )

    def _find_exists(self) -> Optional[Text]:
        """Find an existing request ID in environment variables."""

        for key in self._KEY_NAME_VARIANTS:
            request_id = os.environ.get(key)

            if request_id:
                return request_id

        return None

    @staticmethod
    def _generate() -> Text:
        """Generate a new UUIDv7 request ID."""
        return str(uuid7())

    def get_request_id(self) -> Text:
        """Get an existing request ID or generate a new one."""

        request_id = self._find_exists()

        if request_id is None:
            request_id = self._generate()

        return request_id

    def _get_url_for_log(self, url: Text) -> Text:
        """Return URL prepared for logging."""
        return url
