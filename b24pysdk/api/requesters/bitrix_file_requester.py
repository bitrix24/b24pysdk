from email.message import Message
from typing import TYPE_CHECKING, Dict, Final, Optional, Text
from urllib.parse import urlsplit, urlunsplit

import requests

from ...errors import BitrixFileDownloadError, BitrixRequestError, BitrixRequestTimeout
from ...utils.types import Number, Timeout
from ._base_requester import BaseRequester

if TYPE_CHECKING:
    from ...schemas.file import BitrixFileResponseData

__all__ = [
    "BitrixFileRequester",
]


class BitrixFileRequester(BaseRequester):
    """Requester for downloading file content from a URL returned by Bitrix24."""

    _HEADERS: Final[Dict[Text, Text]] = {
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    }

    __slots__ = ("_referer", "_url")

    _referer: Text
    _url: Text

    def __init__(
            self,
            url: Text,
            *,
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

        if not (isinstance(url, str) and url):
            raise ValueError("File download URL must be a non-empty string.")

        self._url = url
        self._referer = self._get_referer(url)

    @staticmethod
    def _get_referer(url: Text) -> Text:
        """Return the URL origin used as Referer for a file download."""

        parsed_url = urlsplit(url)

        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("File download URL must be an absolute HTTP(S) URL.")

        return f"{parsed_url.scheme}://{parsed_url.netloc}/"

    @property
    def _headers(self) -> Dict:
        """Return SDK headers required for Bitrix24 file downloads."""
        return super()._headers | self._HEADERS | {"Referer": self._referer}

    def _get_url_for_log(self, url: Text) -> Text:
        """Return file URL prepared for logging without signed query data."""

        if not self._config.secure_log:
            return url

        parsed_url = urlsplit(url)
        return urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", ""))

    def _request(self) -> requests.Response:
        """Execute one HTTP GET for file content."""

        self._config.logger.debug(
            "start bitrix_file_request",
            context={
                "method": "GET",
                "URL": self._get_url_for_log(self._url),
                "timeout": self._timeout,
            },
        )

        response = requests.get(
            url=self._url,
            headers=self._headers,
            timeout=self._timeout,
        )

        self._config.logger.debug(
            "finish bitrix_file_request",
            context={
                "response": str(response),
            },
        )

        return response

    def _get(self) -> requests.Response:
        """Send the download request with SDK transport exception wrapping."""

        try:
            return self._request_with_retries()

        except requests.Timeout as error:
            raise BitrixRequestTimeout(timeout=self._timeout, original_error=error) from error

        except requests.RequestException as error:
            raise BitrixRequestError(original_error=error) from error

    @staticmethod
    def _get_file_name(response: requests.Response) -> Optional[Text]:
        """Return the file name from the Content-Disposition header, if present."""

        content_disposition = response.headers.get("Content-Disposition")

        if not content_disposition:
            return None

        message = Message()
        message["Content-Disposition"] = content_disposition

        return message.get_filename()

    def call(self) -> "BitrixFileResponseData":
        """Execute the request and return downloaded file data."""

        response = self._get()

        if not response.ok:
            raise BitrixFileDownloadError(response=response)

        return {
            "content": response.content,
            "name": self._get_file_name(response),
        }
