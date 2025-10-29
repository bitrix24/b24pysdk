from typing import Text

from ..requesters import BitrixOAuthRequester
from ..responses import BitrixAppInfoResponse
from .renewed_oauth_token import RenewedOAuthToken


class AbstractBitrixApp:
    """"""

    client_id: Text = NotImplemented
    """"""

    client_secret: Text = NotImplemented
    """"""

    @property
    def is_local(self) -> bool:
        """"""
        return bool(getattr(self, "domain", None))

    def get_oauth_token(self, code: Text) -> RenewedOAuthToken:
        """"""
        return RenewedOAuthToken.from_dict(BitrixOAuthRequester(self).get_oauth_token(code))

    def refresh_oauth_token(self, refresh_token: Text) -> RenewedOAuthToken:
        """"""
        return RenewedOAuthToken.from_dict(BitrixOAuthRequester(self).refresh_oauth_token(refresh_token))

    def get_app_info(self, auth_token: Text) -> BitrixAppInfoResponse:
        """"""
        return BitrixAppInfoResponse.from_dict(BitrixOAuthRequester(self).get_app_info(auth_token))


class AbstractBitrixAppLocal(AbstractBitrixApp):
    """"""

    domain: Text
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
