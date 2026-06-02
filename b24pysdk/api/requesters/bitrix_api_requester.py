from typing import IO, Dict, Final, Optional, Text, Tuple

import requests

from ...errors import BitrixRequestError, BitrixRequestTimeout
from ...utils.types import JSONDict, Number, Timeout
from ._base_requester import BaseRequester

__all__ = [
    "BitrixAPIRequester",
]


class BitrixAPIRequester(BaseRequester):
    """
    Requester for Bitrix24 REST API calls.

    Sends JSON POST requests to prepared Bitrix24 REST URLs and converts
    transport-level failures into SDK request exceptions.
    """

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
        """
        Initialize a Bitrix24 REST API requester.

        Args:
            url: Prepared Bitrix24 REST API endpoint URL.
            params: JSON-compatible request body parameters.
            files: Optional files passed to ``requests.post``.
            timeout: Request timeout.
            max_retries: Maximum number of request attempts.
            initial_retry_delay: Delay before the first retry.
            retry_delay_increment: Additional delay added after each used retry.
        """
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
        """Return default SDK headers extended with JSON content type."""
        return self._get_default_headers() | self._HEADERS

    def _request(self) -> requests.Response:
        """
        Execute one raw Bitrix24 REST API POST request.

        Returns:
            Raw HTTP response returned by ``requests``.
        """

        self._config.logger.debug(
            "start bitrix_api_request",
            context={
                "method": "POST",
                "url": self._url,
                "timeout": self._timeout,
            },
        )

        response = requests.post(
            url=self._url,
            json=self._params,
            headers=self._headers,
            files=self._files,
            timeout=self._timeout,
            allow_redirects=self._ALLOW_REDIRECTS,
        )

        self._config.logger.debug(
            "finish bitrix_api_request",
            context={
                "response": str(response),
            },
        )

        return response

    def _post(self) -> requests.Response:
        """
        Send a POST request to the Bitrix24 REST endpoint.

        Returns:
            Raw HTTP response returned by the server.

        Raises:
            BitrixRequestTimeout: If the request times out.
            BitrixRequestError: If ``requests`` fails before receiving a valid
                HTTP response.
        """

        try:
            return self._request_with_retries()

        except requests.Timeout as error:
            raise BitrixRequestTimeout(timeout=self._timeout, original_error=error) from error

        except requests.RequestException as error:
            raise BitrixRequestError(original_error=error) from error

    def call(self) -> JSONDict:
        """
        Execute the request and parse the Bitrix24 response.

        Returns:
            Parsed JSON-compatible response dictionary.
        """
        return self._parse_response(self._post())
