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
    """"""

    client_id: Text = NotImplemented
    """"""

    client_secret: Text = NotImplemented
    """"""

    def __str__(self):
        return f"<{('Market', 'Local')[self.is_local]} {self.__class__.__name__} with client_id={self.client_id}>"

    @property
    def is_local(self) -> bool:
        """"""
        return bool(getattr(self, "domain", None))

    def get_oauth_token(self, code: Text, **kwargs) -> RenewedOAuth:
        """"""
        return RenewedOAuth.from_dict(BitrixOAuthRequester(self, **kwargs).get_oauth_token(code))

    def refresh_oauth_token(self, refresh_token: Text, **kwargs) -> RenewedOAuth:
        """"""
        return RenewedOAuth.from_dict(BitrixOAuthRequester(self, **kwargs).refresh_oauth_token(refresh_token))

    def get_app_info(self, auth_token: Text, **kwargs) -> BitrixAppInfoResponse:
        """"""
        return BitrixAppInfoResponse.from_dict(BitrixOAuthRequester(self, **kwargs).get_app_info(auth_token))


class AbstractBitrixAppLocal(AbstractBitrixApp):
    """"""

    domain: Text = NotImplemented
    """"""


class BitrixApp(AbstractBitrixApp):
    """Local or market bitrix application"""

    def __init__(
            self,
            *,
            client_id: Text,
            client_secret: Text,
    ):
        self.client_id = client_id
        self.client_secret = client_secret


class BitrixAppLocal(AbstractBitrixAppLocal):
    """"""

    def __init__(
            self,
            *,
            domain: Text,
            client_id: Text,
            client_secret: Text,
    ):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
