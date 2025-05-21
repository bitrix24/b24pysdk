import requests
import time
from typing import Dict, IO, Optional, Text, Tuple
from urllib.parse import urlparse
from http import HTTPStatus

from ...error import BitrixTimeout, ConnectionToBitrixError


def request(
        url: Text,
        *,
        params: bytes,
        files: Optional[Dict[Text, Tuple[Text, IO]]] = None,
        timeout: Optional[int]
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
    # TODO: pull default timeout, number of retries, and retry delay options from global config
    client = ApiClient(
        timeout=timeout,
        max_retries=20,
        initial_retry_delay=0.5,
        retry_delay_increment=0.25
    )

    return client.request(url, params=params, files=files)


class ApiClient:
    def __init__(
            self,
            timeout: int,
            max_retries: int,
            initial_retry_delay: float,
            retry_delay_increment: float
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.retries_remaining = max_retries
        self.initial_retry_delay = initial_retry_delay
        self.retry_delay_increment = retry_delay_increment
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
            timeout: int,
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
