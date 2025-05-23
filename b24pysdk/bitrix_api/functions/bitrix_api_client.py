import requests
import time
from typing import Dict, IO, Optional, Text, Tuple, Union
from urllib.parse import urlparse
from http import HTTPStatus

from ...error import BitrixTimeout, ConnectionToBitrixError

from ..config import SdkConfig


def request(
        url: Text,
        *,
        params: bytes,
        files: Optional[Dict[Text, Tuple[Text, IO]]] = None,
        timeout: Union[int, float, None]
) -> requests.Response:
    """
    Performs a call to the Bitrix API

    Args:
        url: url to which the request should be sent
        params: encoded parameters of the request
        files: files attached to the request
        timeout: timeout in seconds

    Returns:
        Response returned by the server
    Raises:
            ConnectionToBitrixError: if failed to establish HTTP connection
            BitrixTimeout: if the request timed out
    """
    client = BitrixApiClient(timeout=timeout)

    return client.request(url, params=params, files=files)


class BitrixApiClient:
    def __init__(self, timeout: Union[int, float, None] = SdkConfig().default_timeout):
        # TODO: add sentinel class for default timeout
        self.config = SdkConfig()
        self.timeout = timeout
        self.max_retries = self.config.max_retries
        self.retries_remaining = self.max_retries
        self.initial_retry_delay = self.config.initial_retry_delay
        self.retry_delay_increment = self.config.retry_delay_increment
        self.response: Optional[requests.Response] = None
        self.url = None
        self.params = None
        self.files = None

    def request(
            self,
            url: Text,
            params: bytes,
            files: Optional[Dict[Text, Tuple[Text, IO]]]
    ) -> requests.Response:

        self.url = url
        self.params = params
        self.files = files

        while self.retries_remaining > 0:

            self.response = self._post(self.url, data=self.params, files=self.files, timeout=self.timeout)

            if self.response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
                time.sleep(self._retry_timeout)
                self.retries_remaining -= 1

            elif self.response.status_code in (
                HTTPStatus.MOVED_PERMANENTLY,
                HTTPStatus.FOUND,
                HTTPStatus.TEMPORARY_REDIRECT,
                HTTPStatus.PERMANENT_REDIRECT
            ):
                new_url = self._get_redirect_url()
                if new_url:
                    self.url = new_url
                else:
                    break

            else:
                break

        return self.response

    @staticmethod
    def _post(
            url: Text,
            *,
            data: bytes,
            files: Optional[Dict[Text, Tuple[Text, IO]]],
            timeout: Union[int, float, None],
    ) -> requests.Response:
        """Makes a POST-request to given url
            Args:
                url: url to which the request should be sent
                data: encoded parameters of the request
                files: files attached to the request
                timeout: timeout in seconds
            Returns:
                Response returned by the server
            Raises:
                ConnectionToBitrixError: if failed to establish HTTP connection
                BitrixTimeout: if the request timed out
        """

        try:
            return requests.post(
                url=url,
                data=data,
                timeout=timeout,
                files=files,
                allow_redirects=False,
            )

        except requests.ConnectionError as error:
            raise ConnectionToBitrixError(original_error=error) from error

        except requests.Timeout as error:
            raise BitrixTimeout(timeout=timeout, original_error=error) from error

    def _get_redirect_url(self) -> Optional[Text]:
        """
        Retrieves url to be redirected to from the response's 'location' header
        If server redirects to the same domain, returns None

        Returns:
            URL to be redirected to, None if 'location' header is not set or if response redirects to the same domain
        """
        if not self.response:
            return None
        location = self.response.headers.get("location")
        if not location:
            return None

        old_domain = urlparse(self.url).netloc
        new_domain = urlparse(location).netloc

        return location if old_domain != new_domain else None

    @property
    def _retry_timeout(self) -> float:
        """Calculates timeout between retries based on amount of retries used

        Returns:
            time to wait before next request in seconds
        """
        used_retries = self.max_retries - self.retries_remaining

        return self.initial_retry_delay + used_retries * self.retry_delay_increment
