from typing import IO, Dict, Final, Optional, Text, Tuple

import requests

from ...error import BitrixRequestError, BitrixRequestTimeout
from ...utils.types import JSONDict, Number, Timeout
from ._base_requester import BaseRequester

__all__ = [
    "BitrixAPIRequester",
]


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
        Makes a POST-requests to given url

        Returns:
            Response returned by the server

        Raises:
            ConnectionToBitrixError: if failed to establish HTTP connection

            BitrixRequestTimeout: if the requests timed out
        """

        try:
            return self._request_with_retries()

        except requests.Timeout as error:
            raise BitrixRequestTimeout(timeout=self._timeout, original_error=error) from error

        except requests.RequestException as error:
            raise BitrixRequestError(original_error=error) from error

    def call(self) -> JSONDict:
        """"""
        return self._parse_response(self._post())
