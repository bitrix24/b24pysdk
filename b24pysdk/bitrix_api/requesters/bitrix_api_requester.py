from http import HTTPStatus
from typing import IO, Dict, Final, Optional, Text, Tuple
from urllib.parse import urlparse

import requests

from ...error import BitrixRequestError, BitrixTimeout
from ...utils.types import JSONDict, Number, Timeout
from ._base_requester import BaseRequester


class BitrixAPIRequester(BaseRequester):
    """"""

    _ALLOW_REDIRECTS: Final[bool] = False
    _HEADERS: Final[Dict] = {"Content-Type": "application/json"}

    __slots__ = ("_files", "_params", "_url")

    _files: Optional[Dict[Text, Tuple[Text, IO]]]
    _params: Optional[JSONDict]
    _url: Text

    def __init__(
            self,
            url: Text,
            *,
            params: Optional[JSONDict] = None,
            files: Optional[Dict[Text, Tuple[Text, IO]]] = None,
            timeout: Timeout = None,
            max_retries: Optional[int] = None,
            initial_retry_delay: Optional[Number] = None,
            retry_delay_increment: Optional[Number] = None,
    ):
        super().__init__(
            timeout=timeout,
            max_retries=max_retries,
            initial_retry_delay=initial_retry_delay,
            retry_delay_increment=retry_delay_increment,
        )
        self._url = url
        self._params = params
        self._files = files

    @property
    def _headers(self) -> Dict:
        """"""
        return self._get_default_headers() | self._HEADERS

    def _request(self) -> requests.Response:
        return requests.post(
            url=self._url,
            json=self._params,
            timeout=self._timeout,
            files=self._files,
            allow_redirects=self._ALLOW_REDIRECTS,
            headers=self._headers,
        )

    def _post(self) -> requests.Response:
        """
        Makes a POST-request to given url

        Returns:
            Response returned by the server

        Raises:
            ConnectionToBitrixError: if failed to establish HTTP connection

            BitrixTimeout: if the request timed out
        """

        try:
            return self._request_with_retries()

        except requests.Timeout as error:
            raise BitrixTimeout(timeout=self._timeout, original_error=error) from error

        except requests.RequestException as error:
            raise BitrixRequestError(original_error=error) from error

    def _get_redirect_url(self, response: requests.Response) -> Optional[Text]:
        """
        Retrieves url to be redirected to from the response's 'location' header
        If server redirects to the same domain, returns None

        Returns:
            URL to be redirected to, None if 'location' header is not set or if response redirects to the same domain
        """

        if not response:
            return None

        location = response.headers.get("location")

        if not location:
            return None

        old_domain = urlparse(self._url).netloc
        new_domain = urlparse(location).netloc

        if old_domain != new_domain:
            return location
        else:
            return None

    def call(self) -> requests.Response:
        """"""

        response = self._post()

        if response.status_code in (
                HTTPStatus.MOVED_PERMANENTLY,
                HTTPStatus.FOUND,
                HTTPStatus.TEMPORARY_REDIRECT,
                HTTPStatus.PERMANENT_REDIRECT,
        ):
            new_url = self._get_redirect_url(response)

            if new_url:
                self._url = new_url
                response = self._post()

        return response
