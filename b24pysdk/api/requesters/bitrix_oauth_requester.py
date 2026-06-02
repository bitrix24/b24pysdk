from typing import Any, Dict, Final, Optional, Text

import requests

from ...errors import (
    BitrixAPIInsufficientScope,
    BitrixAPIInvalidRequest,
)
from ...errors.oauth import (
    BitrixOAuthInsufficientScope,
    BitrixOAuthInvalidRequest,
    BitrixOAuthRequestError,
    BitrixOAuthRequestTimeout,
)
from ...protocols import BitrixOAuthProtocol
from ...utils.types import JSONDict, Number, Timeout
from ._base_requester import BaseRequester

__all__ = [
    "BitrixOAuthRequester",
]


class BitrixOAuthRequester(BaseRequester):
    """
    Requester for Bitrix24 OAuth endpoints.

    Handles authorization-code exchange, token refresh, and ``app.info`` calls
    through the Bitrix24 OAuth host.
    """

    _HEADERS: Final[Dict] = {"Content-Type": "application/x-www-form-urlencoded"}
    _BASE_OAUTH_URL: Final[Text] = "https://oauth.bitrix24.tech"
    _OAUTH_TOKEN_URL: Final[Text] = f"{_BASE_OAUTH_URL}/oauth/token/"
    _APP_INFO_URL: Final[Text] = f"{_BASE_OAUTH_URL}/rest/app.info/"
    _MASKED_VALUE: Final[Text] = "********"
    _SENSITIVE_LOG_KEYS: Final[frozenset[Text]] = frozenset({
        "access_token",
        "auth",
        "auth_token",
        "client_secret",
        "code",
        "refresh_token",
    })

    __slots__ = ("_bitrix_oauth",)

    _bitrix_oauth: BitrixOAuthProtocol

    def __init__(
            self,
            bitrix_oauth: BitrixOAuthProtocol,
            *,
            timeout: Timeout = None,
            max_retries: Optional[int] = None,
            initial_retry_delay: Optional[Number] = None,
            retry_delay_increment: Optional[Number] = None,
    ):
        """
        Initialize OAuth requester.

        Args:
            bitrix_oauth: Object exposing Bitrix24 OAuth client credentials.
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
        self._bitrix_oauth = bitrix_oauth

    @property
    def _headers(self) -> Dict:
        """Return default SDK headers extended with form content type."""
        return self._get_default_headers() | self._HEADERS

    def _request(self, url: Text, params: JSONDict) -> requests.Response:
        """
        Execute one raw OAuth GET request.

        Args:
            url: OAuth endpoint URL.
            params: Query parameters sent to the endpoint.

        Returns:
            Raw HTTP response returned by ``requests``.
        """

        self._config.logger.debug(
            "start bitrix_oauth_request",
            context={
                "method": "GET",
                "url": url,
                "timeout": self._timeout,
            },
        )

        response = requests.get(
            url=url,
            params=params,
            headers=self._headers,
            timeout=self._timeout,
        )

        self._config.logger.debug(
            "finish bitrix_oauth_request",
            context={
                "response": str(response),
            },
        )

        return response

    def _get(self, url: Text, params: JSONDict) -> requests.Response:
        """
        Send an OAuth GET request with SDK error wrapping.

        Args:
            url: OAuth endpoint URL.
            params: Query parameters sent to the endpoint.

        Returns:
            Raw HTTP response returned by the server.

        Raises:
            BitrixOAuthRequestTimeout: If the request times out.
            BitrixOAuthRequestError: If ``requests`` fails before receiving a
                valid HTTP response.
        """

        try:
            return self._request_with_retries(url=url, params=params)

        except requests.Timeout as error:
            raise BitrixOAuthRequestTimeout(timeout=self._timeout, original_error=error) from error

        except requests.RequestException as error:
            raise BitrixOAuthRequestError(original_error=error) from error

    @classmethod
    def _parse_response(cls, response: requests.Response) -> JSONDict:
        """
        Parse OAuth response and map common API errors to OAuth-specific errors.

        Args:
            response: Raw HTTP response returned by ``requests``.

        Returns:
            Parsed JSON-compatible response dictionary.

        Raises:
            BitrixOAuthInvalidRequest: If the OAuth endpoint returns an invalid
                request error.
            BitrixOAuthInsufficientScope: If the OAuth endpoint reports missing
                permissions.
        """

        try:
            return super()._parse_response(response)

        except BitrixAPIInvalidRequest as error:
            raise BitrixOAuthInvalidRequest(response=error.response, json_response=error.json_response) from error

        except BitrixAPIInsufficientScope as error:
            raise BitrixOAuthInsufficientScope(response=error.response, json_response=error.json_response) from error

    @classmethod
    def _mask_sensitive_value(cls, value: Any) -> Any:
        """Return a masked representation for non-empty sensitive values."""
        return cls._MASKED_VALUE if value else value

    @classmethod
    def _mask_sensitive_data(cls, data: Any) -> Any:
        """Recursively mask sensitive values while preserving response shape."""

        if isinstance(data, dict):
            return {
                key: cls._mask_sensitive_value(value)
                if str(key).lower() in cls._SENSITIVE_LOG_KEYS
                else cls._mask_sensitive_data(value)
                for key, value in data.items()
            }

        if isinstance(data, list):
            return [cls._mask_sensitive_data(item) for item in data]

        return data

    def get_oauth_token(self, code: Text) -> JSONDict:
        """
        Exchange an authorization code for OAuth tokens.

        Args:
            code: Authorization code received from Bitrix24.

        Returns:
            Parsed OAuth token response.
        """

        params: JSONDict = {
            "grant_type": "authorization_code",
            "client_id": self._bitrix_oauth.client_id,
            "client_secret": self._bitrix_oauth.client_secret,
            "code": code,
        }

        self._config.logger.debug(
            "start get_oauth_token",
            context={
                "bitrix_oauth": str(self._bitrix_oauth),
                "code": self._mask_sensitive_value(code),
            },
        )

        json_response = self._parse_response(self._get(url=self._OAUTH_TOKEN_URL, params=params))

        self._config.logger.debug(
            "finish get_oauth_token",
            context={
                "json_response": self._mask_sensitive_data(json_response),
            },
        )

        return json_response

    def refresh_oauth_token(self, refresh_token: Text) -> JSONDict:
        """
        Refresh OAuth tokens using a refresh token.

        Args:
            refresh_token: Refresh token issued by Bitrix24.

        Returns:
            Parsed OAuth token response with renewed token data.
        """

        params: JSONDict = {
            "grant_type": "refresh_token",
            "client_id": self._bitrix_oauth.client_id,
            "client_secret": self._bitrix_oauth.client_secret,
            "refresh_token": refresh_token,
        }

        self._config.logger.debug(
            "start refresh_oauth_token",
            context={
                "bitrix_oauth": str(self._bitrix_oauth),
                "refresh_token": self._mask_sensitive_value(refresh_token),
            },
        )

        json_response = self._parse_response(self._get(url=self._OAUTH_TOKEN_URL, params=params))

        self._config.logger.debug(
            "finish refresh_oauth_token",
            context={
                "json_response": self._mask_sensitive_data(json_response),
            },
        )

        return json_response

    def get_app_info(self, auth_token: Text) -> JSONDict:
        """
        Retrieve Bitrix24 application installation information.

        Args:
            auth_token: OAuth access token used for the ``app.info`` request.

        Returns:
            Parsed ``app.info`` response.
        """

        params: JSONDict = {
            "auth": auth_token,
        }

        self._config.logger.debug(
            "start get_app_info",
            context={
                "bitrix_oauth": str(self._bitrix_oauth),
                "auth_token": self._mask_sensitive_value(auth_token),
            },
        )

        json_response = self._parse_response(self._get(url=self._APP_INFO_URL, params=params))

        self._config.logger.debug(
            "finish get_app_info",
            context={
                "result": json_response.get("result"),
                "time": json_response.get("time"),
            },
        )

        return json_response
