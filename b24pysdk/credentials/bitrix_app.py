from typing import Text

from ..api.requesters import BitrixOAuthRequester
from ..api.responses import BitrixAppInfoResponse
from .auth import RenewedOAuth

__all__ = [
    "AbstractBitrixApp",
    "AbstractBitrixAppLocal",
    "BitrixApp",
    "BitrixAppLocal",
]


class AbstractBitrixApp:
    """
    Base class for Bitrix24 applications.

    Provides common OAuth-related methods for both market and local apps.
    """

    client_id: Text = NotImplemented
    """OAuth client ID issued by Bitrix24."""

    client_secret: Text = NotImplemented
    """OAuth client secret issued by Bitrix24."""

    def __str__(self):
        return f"<{('Market', 'Local')[self.is_local]} {self.__class__.__name__} with client_id={self.client_id}>"

    @property
    def is_local(self) -> bool:
        """
        Indicates whether the application is a local (on-premise) app.

        Returns:
            True if the app has a domain defined, otherwise False.
        """
        return bool(getattr(self, "domain", None))

    def get_oauth_token(self, code: Text, **kwargs) -> RenewedOAuth:
        """
        Exchange authorization code for an OAuth token.

        Args:
            code: Authorization code received from Bitrix24.
            **kwargs: Additional parameters passed to the requester.

        Returns:
            RenewedOAuth object containing access and refresh tokens.
        """
        return RenewedOAuth.from_dict(BitrixOAuthRequester(self, **kwargs).get_oauth_token(code))

    def refresh_oauth_token(self, refresh_token: Text, **kwargs) -> RenewedOAuth:
        """
        Refresh an existing OAuth token.

        Args:
            refresh_token: Refresh token issued by Bitrix24.
            **kwargs: Additional parameters passed to the requester.

        Returns:
            RenewedOAuth object with updated token data.
        """
        return RenewedOAuth.from_dict(BitrixOAuthRequester(self, **kwargs).refresh_oauth_token(refresh_token))

    def get_app_info(self, auth_token: Text, **kwargs) -> BitrixAppInfoResponse:
        """
        Retrieve application installation information.

        Args:
            auth_token: Access token used for authentication.
            **kwargs: Additional parameters passed to the requester.

        Returns:
            BitrixAppInfoResponse containing application metadata.
        """
        return BitrixAppInfoResponse.from_dict(BitrixOAuthRequester(self, **kwargs).get_app_info(auth_token))


class AbstractBitrixAppLocal(AbstractBitrixApp):
    """
    Base class for local Bitrix24 applications.

    Extends AbstractBitrixApp with required domain attribute.
    """

    domain: Text = NotImplemented
    """Bitrix24 portal domain (e.g., 'example.bitrix24.com')."""


class BitrixApp(AbstractBitrixApp):
    """
    Bitrix24 application (market or standalone OAuth app).

    Can be used for standard OAuth flows without a fixed domain.
    """

    def __init__(
            self,
            *,
            client_id: Text,
            client_secret: Text,
    ):
        """
        Initialize BitrixApp.

        Args:
            client_id: OAuth client ID.
            client_secret: OAuth client secret.
        """
        self.client_id = client_id
        self.client_secret = client_secret


class BitrixAppLocal(AbstractBitrixAppLocal):
    """Local Bitrix24 application bound to a specific portal domain."""

    def __init__(
            self,
            *,
            domain: Text,
            client_id: Text,
            client_secret: Text,
    ):
        """
        Initialize BitrixAppLocal.

        Args:
            domain: Bitrix24 portal domain.
            client_id: OAuth client ID.
            client_secret: OAuth client secret.
        """
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
