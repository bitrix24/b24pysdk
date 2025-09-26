import os
import time
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Dict, Final, Optional, Text, Tuple

import requests
from uuid6 import uuid7

from ..._config import Config
from ..._constants import TEXT_PYTHON_VERSION
from ...utils.types import DefaultTimeout, Number, Timeout
from ...version import SDK_VERSION


class BaseRequester(ABC):
    """"""

    _DEFAULT_REQUEST_ID_HEADER_FIELD_NAME: Final[Text] = "X-Request-ID"
    _SDK_VERSION: Final[Text] = SDK_VERSION
    _SDK_USER_AGENT: Final[Text] = "b24-python-sdk-vendor"
    _TEXT_PYTHON_VERSION: Final[Text] = TEXT_PYTHON_VERSION

    _KEY_NAME_VARIANTS: Final[Tuple[Text, ...]] = (
        "REQUEST_ID",
        "HTTP_X_REQUEST_ID",
        "UNIQUE_ID",
    )

    __slots__ = ("_config", "_initial_retry_delay", "_max_retries", "_retries_remaining", "_retry_delay_increment", "_timeout")

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
        self._config = Config()
        self._timeout = timeout or self._config.default_timeout
        self._max_retries = max_retries or self._config.max_retries
        self._retries_remaining = self._max_retries
        self._initial_retry_delay = initial_retry_delay or self._config.initial_retry_delay
        self._retry_delay_increment = retry_delay_increment or self._config.retry_delay_increment

    @property
    @abstractmethod
    def _headers(self) -> Dict:
        """"""
        raise NotImplementedError

    def _get_default_headers(self) -> Dict[Text, Text]:
        """"""
        return {
            "Accept": "application/json",
            "Accept-Charset": "utf-8",
            "User-Agent": f"{self._SDK_USER_AGENT}-v-{self._SDK_VERSION}-python-{self._TEXT_PYTHON_VERSION}",
            "X-BITRIX24-PYTHON-SDK-PYTHON-VERSION": self._TEXT_PYTHON_VERSION,
            "X-BITRIX24-PYTHON-SDK-VERSION": self._SDK_VERSION,
            self._DEFAULT_REQUEST_ID_HEADER_FIELD_NAME: self.get_request_id(),
        }

    @abstractmethod
    def _request(self, *args, **kwargs) -> requests.Response:
        """"""
        raise NotImplementedError

    @property
    def _retry_timeout(self) -> float:
        """
        Calculates timeout between retries based on amount of retries used

        Returns:
            time to wait before next request in seconds
        """
        used_retries = self._max_retries - self._retries_remaining
        return self._initial_retry_delay + used_retries * self._retry_delay_increment

    def _request_with_retries(self, *args, **kwargs) -> requests.Response:
        """"""

        self._retries_remaining = self._max_retries

        while self._retries_remaining > 0:

            self._retries_remaining -= 1
            response = self._request(*args, **kwargs)

            if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE and self._retries_remaining:
                time.sleep(self._retry_timeout)
            else:
                return response

        raise RuntimeError(
            f"Request failed after {self._max_retries} attempts. "
            "No valid response was received from the server.",
        )

    def _find_exists(self) -> Optional[Text]:
        """Find an existing request id in environment variables."""

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
        """Get existing request id or generate a new one."""

        request_id = self._find_exists()

        if request_id is None:
            request_id = self._generate()

        return request_id
