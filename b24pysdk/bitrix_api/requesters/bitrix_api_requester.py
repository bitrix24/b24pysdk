import time
from http import HTTPStatus
from typing import IO, Dict, Final, Optional, Text, Tuple
from urllib.parse import urlparse

import requests

from ..._config import Config
from ...error import BitrixRequestError, BitrixTimeout
from ...utils.types import JSONDict, Timeout
from ._base_requester import BaseRequester


class BitrixAPIRequester(BaseRequester):
    """"""

    _HEADERS: Final[Dict] = {"Content-Type": "application/json"}
    _ALLOW_REDIRECTS: Final[bool] = False

    def __init__(
            self,
            url: Text,
            *,
            params: Optional[JSONDict] = None,
            files: Optional[Dict[Text, Tuple[Text, IO]]] = None,
            timeout: Timeout = None,
            max_retries: Optional[int] = None,
            initial_retry_delay: Optional[float] = None,
            retry_delay_increment: Optional[float] = None,
    ):
        self._config = Config()
        self._url = url
        self._params = params
        self._files = files
        self._timeout = timeout or self._config.default_timeout
        self._max_retries = max_retries or self._config.max_retries
        self._retries_remaining = self._max_retries
        self._initial_retry_delay = initial_retry_delay or self._config.initial_retry_delay
        self._retry_delay_increment = retry_delay_increment or self._config.retry_delay_increment
        self._response: Optional[requests.Response] = None

    @property
    def _headers(self) -> Dict:
        """"""
        return self._get_default_headers() | self._HEADERS

    def _get_redirect_url(self) -> Optional[Text]:
        """
        Retrieves url to be redirected to from the response's 'location' header
        If server redirects to the same domain, returns None

        Returns:
            URL to be redirected to, None if 'location' header is not set or if response redirects to the same domain
        """

        if not self._response:
            return None

        location = self._response.headers.get("location")

        if not location:
            return None

        old_domain = urlparse(self._url).netloc
        new_domain = urlparse(location).netloc

        if old_domain != new_domain:
            return location
        else:
            return None

    @property
    def _retry_timeout(self) -> float:
        """Calculates timeout between retries based on amount of retries used

        Returns:
            time to wait before next request in seconds
        """
        used_retries = self._max_retries - self._retries_remaining
        return self._initial_retry_delay + used_retries * self._retry_delay_increment

    def _post(self) -> requests.Response:
        """Makes a POST-request to given url
            Returns:
                Response returned by the server
            Raises:
                ConnectionToBitrixError: if failed to establish HTTP connection
                BitrixTimeout: if the request timed out
        """

        self._retries_remaining -= 1

        try:
            return requests.post(
                url=self._url,
                json=self._params,
                timeout=self._timeout,
                files=self._files,
                allow_redirects=self._ALLOW_REDIRECTS,
                headers=self._headers,
            )

        except requests.Timeout as error:
            raise BitrixTimeout(timeout=self._timeout, original_error=error) from error

        except requests.RequestException as error:
            raise BitrixRequestError(original_error=error) from error

    def call(self) -> requests.Response:
        """"""

        while self._retries_remaining > 0:

            self._response = self._post()

            if self._response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
                time.sleep(self._retry_timeout)

            elif self._response.status_code in (
                    HTTPStatus.MOVED_PERMANENTLY,
                    HTTPStatus.FOUND,
                    HTTPStatus.TEMPORARY_REDIRECT,
                    HTTPStatus.PERMANENT_REDIRECT,
            ):
                new_url = self._get_redirect_url()

                if new_url:
                    self._url = new_url
                else:
                    break
            else:
                break

        return self._response
