from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Dict, Final, Mapping, Optional, Sequence, Text, overload

from ..._config import Config
from ...error import BitrixAPIExpiredToken, BitrixResponse302JSONDecodeError
from ...utils.types import B24BatchMethods, B24BatchMethodTuple, JSONDict, Key, Timeout
from ..events import OAuthTokenRenewedEvent, PortalDomainChangedEvent
from ..functions import call_batch, call_batches, call_list, call_list_fast, call_method
from ..signals import BitrixSignalInstance
from .bitrix_app import AbstractBitrixApp, AbstractBitrixAppLocal
from .oauth_token import OAuthToken

if TYPE_CHECKING:
    from ..responses import BitrixAppInfoResponse
    from .oauth_placememt_data import OAuthPlacementData
    from .renewed_oauth_token import RenewedOAuthToken


def _bitrix_app_required(func: Callable):
    """"""
    @wraps(func)
    def wrapper(self: "AbstractBitrixToken", *args, **kwargs):
        if not getattr(self, "bitrix_app", None):
            raise AttributeError(f"'bitrix_app' is not defined for {self}")
        return func(self, *args, **kwargs)
    return wrapper


class AbstractBitrixToken:
    """"""

    _AUTO_REFRESH: bool = True
    """"""

    domain: Text = NotImplemented
    """"""

    auth_token: Text = NotImplemented
    """"""

    refresh_token: Optional[Text] = NotImplemented
    """"""

    bitrix_app: Optional[AbstractBitrixApp]
    """"""

    oauth_token_renewed_signal: BitrixSignalInstance = BitrixSignalInstance.create_signal(OAuthTokenRenewedEvent)
    """"""

    portal_domain_changed_signal: BitrixSignalInstance = BitrixSignalInstance.create_signal(PortalDomainChangedEvent)
    """"""

    def __str__(self):
        return f"<{'Webhook' if self.is_webhook else 'Application'} token of portal {self.domain}>"

    @property
    def is_webhook(self) -> bool:
        """"""
        return not bool(getattr(self, "bitrix_app", None))

    @property
    def _auth_data(self) -> Dict:
        """"""
        return dict(
            domain=self.domain,
            auth_token=self.auth_token,
            is_webhook=self.is_webhook,
            bitrix_token=self,
        )

    @property
    def _config(self):
        return Config()

    @property
    def oauth_token(self) -> OAuthToken:
        """"""
        return OAuthToken(
            access_token=self.auth_token,
            refresh_token=self.refresh_token,
            expires=None,
        )

    @oauth_token.setter
    def oauth_token(self, oauth_token: OAuthToken):
        """"""
        self.auth_token = oauth_token.access_token
        self.refresh_token = oauth_token.refresh_token

    @_bitrix_app_required
    def get_oauth_token(self, code: Text) -> "RenewedOAuthToken":
        """"""
        return self.bitrix_app.get_oauth_token(code=code)

    @_bitrix_app_required
    def refresh_oauth_token(self) -> "RenewedOAuthToken":
        """"""
        return self.bitrix_app.refresh_oauth_token(refresh_token=self.refresh_token)

    @_bitrix_app_required
    def get_app_info(self) -> "BitrixAppInfoResponse":
        """"""
        return self._execute_with_retries(lambda: self.bitrix_app.get_app_info(self.auth_token))

    def _refresh_and_set_oauth_token(self):
        """"""

        renewed_oauth_token = self.refresh_oauth_token()

        self.oauth_token = renewed_oauth_token.oauth_token

        self.oauth_token_renewed_signal.emit(OAuthTokenRenewedEvent(
            renewed_oauth_token=renewed_oauth_token,
        ))

    def _check_and_change_domain(self, new_domain: Text) -> bool:
        if not new_domain or new_domain == self.domain:
            return False

        old_domain = self.domain
        self.domain = new_domain

        self.portal_domain_changed_signal.emit(PortalDomainChangedEvent(
            old_domain=old_domain,
            new_domain=new_domain,
        ))

        return True

    def _execute_with_retries(self, call_func: Callable[[], Any]):
        """"""

        try:
            return call_func()

        except BitrixResponse302JSONDecodeError as error:
            if self._check_and_change_domain(error.new_domain):
                self._config.logger.info(
                    "Domain changed, retrying request",
                    context=dict(old_domain=self.domain, new_domain=error.new_domain),
                )
                return call_func()
            else:
                self._config.logger.warning(
                    "Caught BitrixResponse302JSONDecodeError, but domain did not change!",
                    context=dict(old_domain=self.domain, new_domain=error.new_domain),
                )
                raise

        except BitrixAPIExpiredToken:
            if self._AUTO_REFRESH and not self.is_webhook:
                self._config.logger.info(
                    "Token expired, auto-refreshing token",
                    context=dict(domain=self.domain, auto_refresh=self._AUTO_REFRESH, is_webhook=self.is_webhook),
                )
                self._refresh_and_set_oauth_token()
                return call_func()
            else:
                self._config.logger.warning(
                    "Token expired, but auto-refresh disabled!",
                    context=dict(domain=self.domain, auto_refresh=self._AUTO_REFRESH, is_webhook=self.is_webhook),
                )
                raise

    def _call_with_retries(self, call_func: Callable, parameters: Dict) -> JSONDict:
        """"""
        return self._execute_with_retries(lambda: call_func(**self._auth_data, **parameters))

    def call_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            *,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_retries(
            call_func=call_method,
            parameters=dict(
                api_method=api_method,
                params=params,
                timeout=timeout,
                **kwargs,
            ),
        )

    @overload
    def call_batch(
            self,
            methods: Mapping[Key, B24BatchMethodTuple],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict: ...

    @overload
    def call_batch(
            self,
            methods: Sequence[B24BatchMethodTuple],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict: ...

    def call_batch(
            self,
            methods: B24BatchMethods,
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_retries(
            call_func=call_batch,
            parameters=dict(
                methods=methods,
                halt=halt,
                ignore_size_limit=ignore_size_limit,
                timeout=timeout,
                **kwargs,
            ),
        )

    @overload
    def call_batches(
            self,
            methods: Mapping[Key, B24BatchMethodTuple],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict: ...

    @overload
    def call_batches(
            self,
            methods: Sequence[B24BatchMethodTuple],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict: ...

    def call_batches(
            self,
            methods: B24BatchMethods,
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_retries(
            call_func=call_batches,
            parameters=dict(
                methods=methods,
                halt=halt,
                timeout=timeout,
                **kwargs,
            ),
        )

    def call_list(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            *,
            limit: Optional[int] = None,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_retries(
            call_func=call_list,
            parameters=dict(
                api_method=api_method,
                params=params,
                limit=limit,
                timeout=timeout,
                **kwargs,
            ),
        )

    def call_list_fast(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            *,
            descending: bool = False,
            limit: Optional[int] = None,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_retries(
            call_func=call_list_fast,
            parameters=dict(
                api_method=api_method,
                params=params,
                descending=descending,
                limit=limit,
                timeout=timeout,
                **kwargs,
            ),
        )


class AbstractBitrixTokenLocal(AbstractBitrixToken):
    """"""

    bitrix_app: AbstractBitrixAppLocal
    """"""

    @property
    def domain(self) -> Text:
        """"""
        return self.bitrix_app.domain

    @domain.setter
    def domain(self, domain: Text):
        """"""
        self.bitrix_app.domain = domain


class BitrixToken(AbstractBitrixToken):
    """"""

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            refresh_token: Optional[Text] = None,
            bitrix_app: Optional[AbstractBitrixApp] = None,
    ):
        self.domain = domain
        self.auth_token = auth_token
        self.refresh_token = refresh_token
        self.bitrix_app = bitrix_app

    @classmethod
    def from_renewed_oauth_token(
            cls,
            renewed_oauth_token: "RenewedOAuthToken",
            bitrix_app: "AbstractBitrixApp",
    ) -> "BitrixToken":
        """"""
        oauth_token = renewed_oauth_token.oauth_token
        return cls(
            domain=renewed_oauth_token.portal_domain,
            auth_token=oauth_token.access_token,
            refresh_token=oauth_token.refresh_token,
            bitrix_app=bitrix_app,
        )

    @classmethod
    def from_oauth_placement_data(
            cls,
            oauth_placement_data: "OAuthPlacementData",
            bitrix_app: "AbstractBitrixApp",
    ) -> "BitrixToken":
        """"""
        oauth_token = oauth_placement_data.oauth_token
        return cls(
            domain=oauth_placement_data.domain,
            auth_token=oauth_token.access_token,
            refresh_token=oauth_token.refresh_token,
            bitrix_app=bitrix_app,
        )


class BitrixTokenLocal(AbstractBitrixTokenLocal):
    """"""

    def __init__(
            self,
            *,
            auth_token: Text,
            refresh_token: Optional[Text] = None,
            bitrix_app: AbstractBitrixAppLocal,
    ):
        self.auth_token = auth_token
        self.refresh_token = refresh_token
        self.bitrix_app = bitrix_app

    @classmethod
    def from_renewed_oauth_token(
            cls,
            renewed_oauth_token: "RenewedOAuthToken",
            bitrix_app: "AbstractBitrixAppLocal",
    ) -> "BitrixTokenLocal":
        """"""
        oauth_token = renewed_oauth_token.oauth_token
        return cls(
            auth_token=oauth_token.access_token,
            refresh_token=oauth_token.refresh_token,
            bitrix_app=bitrix_app,
        )

    @classmethod
    def from_oauth_placement_data(
            cls,
            oauth_placement_data: "OAuthPlacementData",
            bitrix_app: "AbstractBitrixAppLocal",
    ) -> "BitrixTokenLocal":
        """"""
        oauth_token = oauth_placement_data.oauth_token
        return cls(
            auth_token=oauth_token.access_token,
            refresh_token=oauth_token.refresh_token,
            bitrix_app=bitrix_app,
        )


class BitrixWebhook(BitrixToken):
    """"""

    __AUTH_TOKEN_PARTS_COUNT: Final[int] = 2

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
    ):
        super().__init__(domain=domain, auth_token=auth_token)

    @property
    def user_id(self) -> int:
        """"""

        auth_parts = self.auth_token.strip("/").split("/")

        if len(auth_parts) == self.__AUTH_TOKEN_PARTS_COUNT and auth_parts[0].isdigit():
            return int(auth_parts[0])
        else:
            raise ValueError(f"Invalid webhook auth_token format: expected 'user_id/webhook_key', got '{self.auth_token}'")

    @property
    def webhook_key(self) -> Text:
        """"""

        auth_parts = self.auth_token.strip("/").split("/")

        if len(auth_parts) == self.__AUTH_TOKEN_PARTS_COUNT:
            return auth_parts[1]
        else:
            raise ValueError(f"Invalid webhook auth_token format: expected 'user_id/webhook_key', got '{self.auth_token}'")
