from http import HTTPStatus
import requests
import time
from typing import Dict, IO, Optional, Text, Tuple
from urllib.parse import urlparse

from ...error import BitrixTimeout, RequestToBitrixError
from ...utils.types import JSONDict, Timeout

from ..config import SdkConfig


def call(
        url: Text,
        *,
        params: Optional[JSONDict] = None,
        files: Optional[Dict[Text, Tuple[Text, IO]]] = None,
        timeout: Timeout = None,
        max_retries: Optional[int] = None,
        initial_retry_delay: Optional[float] = None,
        retry_delay_increment: Optional[float] = None,
) -> requests.Response:
    """
    Performs a call to the Bitrix API

    Args:
        url: url to which the request should be sent
        params: dict of method parameters
        files: files attached to the request
        timeout: timeout in seconds
        max_retries:
        initial_retry_delay:
        retry_delay_increment:

    Returns:
        Response returned by the server
    Raises:
            ConnectionToBitrixError: if failed to establish HTTP connection
            BitrixTimeout: if the request timed out
    """

    bitrix_api_requester = BitrixApiRequester(
        url=url,
        params=params,
        files=files,
        timeout=timeout,
        max_retries=max_retries,
        initial_retry_delay=initial_retry_delay,
        retry_delay_increment=retry_delay_increment,
    )

    return bitrix_api_requester.call()


class BitrixApiRequester:
    """"""

    HEADERS = {
        "Content-Type": "application/json",
    }
    ALLOW_REDIRECTS = False

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
        self._config = SdkConfig()
        self._url = url
        self._params = params
        self._files = files
        self._timeout = timeout or self._config.default_timeout
        self._max_retries = max_retries or self._config.max_retries
        self._retries_remaining = self._max_retries
        self._initial_retry_delay = initial_retry_delay or self._config.initial_retry_delay
        self._retry_delay_increment = retry_delay_increment or self._config.retry_delay_increment
        self._response: Optional[requests.Response] = None

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
                allow_redirects=self.ALLOW_REDIRECTS,
                headers=self.HEADERS,
            )

        except requests.Timeout as error:
            raise BitrixTimeout(timeout=self._timeout, original_error=error) from error

        except requests.RequestException as error:
            raise RequestToBitrixError(original_error=error) from error

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
