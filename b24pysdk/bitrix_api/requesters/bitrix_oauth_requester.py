from functools import wraps
from typing import Callable, Dict, Final, Optional, Text

import requests

from ...error import (
    BitrixAPIInsufficientScope,
    BitrixAPIInvalidRequest,
    BitrixOAuthInsufficientScope,
    BitrixOAuthInvalidRequest,
    BitrixOAuthRequestError,
    BitrixOAuthRequestTimeout,
)
from ...utils.types import JSONDict, Number, Timeout
from ..protocols import BitrixOAuthProtocol
from ._base_requester import BaseRequester


def _bitrix_oauth_required(func: Callable):
    """"""
    @wraps(func)
    def wrapper(self: "BitrixOAuthRequester", *args, **kwargs):
        if not getattr(self, "_bitrix_oauth", None):
            raise AttributeError("'bitrix_oauth' is not defined")
        return func(self, *args, **kwargs)
    return wrapper


class BitrixOAuthRequester(BaseRequester):
    """"""

    _HEADERS: Final[Dict] = {"Content-Type": "application/x-www-form-urlencoded"}
    _OUATH_URL: Final[Text] = "https://oauth.bitrix.info/oauth/token/"
    _REST_URL: Final[Text] = "https://oauth.bitrix24.tech/rest/app.info/"

    __slots__ = ("_bitrix_oauth",)

    _bitrix_oauth: BitrixOAuthProtocol

    def __init__(
            self,
            bitrix_oauth: Optional[BitrixOAuthProtocol] = None,
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
        self._bitrix_oauth = bitrix_oauth

    @property
    def _headers(self) -> Dict:
        """"""
        return self._get_default_headers() | self._HEADERS

    def _request(self, url: Text, params: JSONDict) -> requests.Response:
        return requests.get(
            url=url,
            params=params,
            headers=self._headers,
            timeout=self._timeout,
        )

    def _get(self, url: Text, params: JSONDict) -> requests.Response:
        """"""

        try:
            return self._request_with_retries(url=url, params=params)

        except requests.Timeout as error:
            raise BitrixOAuthRequestTimeout(timeout=self._timeout, original_error=error) from error

        except requests.RequestException as error:
            raise BitrixOAuthRequestError(original_error=error) from error

    @classmethod
    def _parse_response(cls, response: requests.Response) -> JSONDict:
        """"""

        try:
            return super()._parse_response(response)

        except BitrixAPIInvalidRequest as error:
            raise BitrixOAuthInvalidRequest(response=error.response, json_response=error.json_response) from error

        except BitrixAPIInsufficientScope as error:
            raise BitrixOAuthInsufficientScope(response=error.response, json_response=error.json_response) from error

    @_bitrix_oauth_required
    def get_oauth_token(self, code: Text) -> JSONDict:
        """"""

        params = {
            "grant_type": "authorization_code",
            "client_id": self._bitrix_oauth.client_id,
            "client_secret": self._bitrix_oauth.client_secret,
            "code": code,
        }

        return self._parse_response(self._get(url=self._OUATH_URL, params=params))

    @_bitrix_oauth_required
    def refresh_oauth_token(self, refresh_token: Text) -> JSONDict:
        """"""

        params = {
            "grant_type": "refresh_token",
            "client_id": self._bitrix_oauth.client_id,
            "client_secret": self._bitrix_oauth.client_secret,
            "refresh_token": refresh_token,
        }

        return self._parse_response(self._get(url=self._OUATH_URL, params=params))

    def get_app_info(self, auth_token: Text) -> JSONDict:
        """"""

        params = {
            "auth": auth_token,
        }

        return self._parse_response(self._get(url=self._REST_URL, params=params))
