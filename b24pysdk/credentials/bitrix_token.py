from datetime import datetime
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Final, Literal, Mapping, Optional, Sequence, Text, Union, overload

from .._config import Config
from ..api.callers import call_batch, call_batches, call_list, call_list_fast, call_method
from ..client import Client
from ..constants.version import B24APIVersion
from ..errors import BitrixAPIExpiredToken, BitrixResponse302JSONDecodeError
from ..events import OAuthTokenRenewedEvent, PortalDomainChangedEvent
from ..signals import BitrixSignalInstance
from ..utils.functional import classproperty
from ..utils.types import B24APIVersionLiteral, B24Requests, B24RequestTuple, JSONDict, Key, Timeout
from .oauth_token import OAuthToken

if TYPE_CHECKING:
    from ..api.responses import BitrixAppInfoResponse
    from ..client import BaseClient, ClientV1, ClientV2, ClientV3
    from .auth import OAuth, RenewedOAuth
    from .bitrix_app import AbstractBitrixApp, AbstractBitrixAppLocal
    from .oauth_event_data import OAuthEventData
    from .oauth_placement_data import OAuthPlacementData
    from .oauth_workflow_data import OAuthWorkflowData

__all__ = [
    "AbstractBitrixToken",
    "AbstractBitrixTokenLocal",
    "BitrixToken",
    "BitrixTokenLocal",
    "BitrixWebhook",
]


def _bitrix_app_required(func: Callable) -> Callable:
    """"""

    @wraps(func)
    def wrapper(self: "AbstractBitrixToken", *args, **kwargs):
        if self.bitrix_app is NotImplemented or self.bitrix_app is None:
            raise AttributeError(f"'bitrix_app' is not implimented for {self}")
        return func(self, *args, **kwargs)

    return wrapper


class AbstractBitrixToken:
    """Base token wrapper with retry logic, token refresh, and client helpers."""

    _AUTO_CHANCHED_DOMAIN: bool = True
    """Automatically switch token domain on 302 redirect to another portal domain."""

    _AUTO_REFRESH_EXPIRED_TOKEN: bool = True
    """Automatically refresh expired OAuth tokens when possible."""

    domain: Text = NotImplemented
    """Bitrix portal domain used for API requests."""

    auth_token: Text = NotImplemented
    """Current access token (OAuth token or webhook token)."""

    refresh_token: Optional[Text] = NotImplemented
    """OAuth refresh token, if available."""

    expires: Optional[datetime] = NotImplemented
    """OAuth access token expiration datetime."""

    expires_in: Optional[int] = NotImplemented
    """OAuth access token lifetime in seconds."""

    bitrix_app: Optional["AbstractBitrixApp"] = NotImplemented
    """Bitrix application object used for OAuth flows."""

    oauth_token_renewed_signal: BitrixSignalInstance = BitrixSignalInstance.create_signal(OAuthTokenRenewedEvent)
    """Signal emitted after successful OAuth token refresh."""

    portal_domain_changed_signal: BitrixSignalInstance = BitrixSignalInstance.create_signal(PortalDomainChangedEvent)
    """Signal emitted after automatic portal domain change."""

    def __str__(self):
        """Return a concise token representation for logs/debug output."""
        return f"<{('Application', 'Webhook')[self.is_webhook]} token of portal {self.domain}>"

    @property
    def is_webhook(self) -> bool:
        """Whether this token is a webhook token (without bound app)."""
        return not bool(getattr(self, "bitrix_app", None))

    @property
    def _auth_data(self) -> JSONDict:
        """Build auth payload used by low-level API callers."""
        return dict(
            domain=self.domain,
            auth_token=self.auth_token,
            is_webhook=self.is_webhook,
            bitrix_token=self,
        )

    # noinspection PyMethodParameters
    @classproperty
    def _config(cls) -> Config:
        """"""
        return Config()

    @property
    def is_one_off(self) -> bool:
        """"""
        return self.refresh_token is None

    @property
    def has_expired(self) -> Optional[bool]:
        """"""
        return self.expires and self.expires <= self._config.get_local_datetime()

    @property
    def oauth_token(self) -> OAuthToken:
        """"""
        return OAuthToken(
            access_token=self.auth_token,
            refresh_token=self.refresh_token,
            expires=self.expires,
            expires_in=self.expires_in,
        )

    @oauth_token.setter
    def oauth_token(self, oauth_token: OAuthToken):
        """"""
        self.auth_token = oauth_token.access_token
        self.refresh_token = oauth_token.refresh_token
        self.expires = oauth_token.expires
        self.expires_in = oauth_token.expires_in

    @overload
    def get_client(
            self,
            *,
            prefer_version: Literal[2, B24APIVersion.V2] = B24APIVersion.V2,
            **kwargs,
    ) -> "ClientV2": ...

    @overload
    def get_client(
            self,
            *,
            prefer_version: Literal[1, B24APIVersion.V1],
            **kwargs,
    ) -> "ClientV1": ...

    @overload
    def get_client(
            self,
            *,
            prefer_version: Literal[3, B24APIVersion.V3],
            **kwargs,
    ) -> "ClientV3": ...

    def get_client(
            self,
            *,
            prefer_version: Union[B24APIVersionLiteral, B24APIVersion] = B24APIVersion.V2,
            **kwargs,
    ) -> "BaseClient":
        """"""
        return Client(self, prefer_version=prefer_version, **kwargs)

    @_bitrix_app_required
    def get_oauth_token(self, code: Text, **kwargs) -> "RenewedOAuth":
        """"""
        return self.bitrix_app.get_oauth_token(code=code, **kwargs)

    @_bitrix_app_required
    def refresh_oauth_token(self, **kwargs) -> "RenewedOAuth":
        """"""
        return self.bitrix_app.refresh_oauth_token(refresh_token=self.refresh_token, **kwargs)

    @_bitrix_app_required
    def get_app_info(self, **kwargs) -> "BitrixAppInfoResponse":
        """"""
        return self._execute_with_retries(lambda: self.bitrix_app.get_app_info(self.auth_token, **kwargs))

    def refresh_and_set_oauth_token(self, **kwargs):
        """"""

        renewed_oauth = self.refresh_oauth_token(**kwargs)

        self.oauth_token = renewed_oauth.oauth_token

        self.oauth_token_renewed_signal.emit(OAuthTokenRenewedEvent(
            renewed_oauth_token=renewed_oauth,
        ))

    def __expired_token_handler(self) -> bool:
        """"""

        if not self._AUTO_REFRESH_EXPIRED_TOKEN:
            self._config.logger.info(
                "Token expired: auto-refresh is disabled",
                context=dict(
                    bitrix_token=str(self),
                    bitrix_app=str(self.bitrix_app),
                ),
            )
            return False

        if self.is_webhook:
            self._config.logger.warning(
                "Token expired: cannot refresh token for webhook",
                context=dict(
                    bitrix_token=str(self),
                    bitrix_app=str(self.bitrix_app),
                ),
            )
            return False

        if self.is_one_off:
            self._config.logger.warning(
                "Token expired: cannot refresh one-off token",
                context=dict(
                    bitrix_token=str(self),
                    bitrix_app=str(self.bitrix_app),
                ),
            )
            return False

        self._config.logger.info(
            "Token expired: refreshing token",
            context=dict(
                bitrix_token=str(self),
                bitrix_app=str(self.bitrix_app),
            ),
        )

        self.refresh_and_set_oauth_token()

        return True

    def _check_and_change_domain(self, new_domain: Text) -> bool:
        """"""

        if not new_domain or new_domain == self.domain:
            return False

        old_domain = self.domain
        self.domain = new_domain

        self.portal_domain_changed_signal.emit(PortalDomainChangedEvent(
            old_domain=old_domain,
            new_domain=new_domain,
        ))

        return True

    def _execute_with_retries(self, func: Callable[[], Any]):
        """"""

        try:
            if self.has_expired:
                self.__expired_token_handler()

            return func()

        except BitrixResponse302JSONDecodeError as error:
            if not self._AUTO_CHANCHED_DOMAIN:
                self._config.logger.info(
                    "Caught BitrixResponse302JSONDecodeError, but auto-domain-change is disabled",
                    context=dict(
                        bitrix_token=str(self),
                        old_domain=self.domain,
                        new_domain=error.new_domain,
                    ),
                )
                raise

            if self._check_and_change_domain(error.new_domain):
                self._config.logger.info(
                    "Domain changed, retrying request",
                    context=dict(
                        bitrix_token=str(self),
                        old_domain=self.domain,
                        new_domain=error.new_domain,
                    ),
                )
                return func()
            else:
                self._config.logger.warning(
                    "Caught BitrixResponse302JSONDecodeError, but domain did not change!",
                    context=dict(
                        bitrix_token=str(self),
                        old_domain=self.domain,
                        new_domain=error.new_domain,
                    ),
                )
                raise

        except BitrixAPIExpiredToken:
            if self.__expired_token_handler():
                return func()
            raise

    def _call_with_retries(self, call_func: Callable[..., JSONDict], parameters: JSONDict) -> JSONDict:
        """"""
        return self._execute_with_retries(lambda: call_func(**self._auth_data, **parameters))

    def call_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict:
        """
        Call a single Bitrix REST API method with automatic retries and token refresh.

        Args:
            api_method: API method name, e.g. crm.deal.add.
            params: API method parameters.
            timeout: Request timeout in seconds.
            prefer_version: Preferred API version to resolve the method against.

        Returns:
            API response payload.
        """
        return self._call_with_retries(
            call_func=call_method,
            parameters=dict(
                api_method=api_method,
                params=params,
                timeout=timeout,
                prefer_version=prefer_version,
                **kwargs,
            ),
        )

    @overload
    def call_batch(
            self,
            methods: Mapping[Key, B24RequestTuple],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict: ...

    @overload
    def call_batch(
            self,
            methods: Sequence[B24RequestTuple],
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict: ...

    def call_batch(
            self,
            methods: B24Requests,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict:
        """
        Call multiple API methods in a single batch request with retries.

        Args:
            methods: Batch methods collection.
            halt: Stop on first error if True.
            ignore_size_limit: Truncate instead of raising when batch size exceeds limit.
            timeout: Request timeout in seconds.
            prefer_version: Preferred API version to resolve the batch method against.

        Returns:
            Batch response payload.
        """
        return self._call_with_retries(
            call_func=call_batch,
            parameters=dict(
                methods=methods,
                halt=halt,
                ignore_size_limit=ignore_size_limit,
                timeout=timeout,
                prefer_version=prefer_version,
                **kwargs,
            ),
        )

    @overload
    def call_batches(
            self,
            methods: Mapping[Key, B24RequestTuple],
            halt: bool = False,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict: ...

    @overload
    def call_batches(
            self,
            methods: Sequence[B24RequestTuple],
            halt: bool = False,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict: ...

    def call_batches(
            self,
            methods: B24Requests,
            halt: bool = False,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict:
        """
        Call multiple API methods using parallel batch requests with retries.

        Args:
            methods: Batch methods collection.
            halt: Stop on first error if True.
            timeout: Request timeout in seconds.
            prefer_version: Preferred API version to resolve the batch method against.

        Returns:
            Batch response payload.
        """
        return self._call_with_retries(
            call_func=call_batches,
            parameters=dict(
                methods=methods,
                halt=halt,
                timeout=timeout,
                prefer_version=prefer_version,
                **kwargs,
            ),
        )

    def call_list(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict:
        """
        Call list-like API methods with pagination and retries.

        Args:
            api_method: API method name, e.g. crm.deal.list.
            params: API method parameters.
            limit: Maximum number of items to return.
            timeout: Request timeout in seconds.
            prefer_version: Preferred API version to resolve the method against.

        Returns:
            API response payload.
        """
        return self._call_with_retries(
            call_func=call_list,
            parameters=dict(
                api_method=api_method,
                params=params,
                limit=limit,
                timeout=timeout,
                prefer_version=prefer_version,
                **kwargs,
            ),
        )

    def call_list_fast(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            descending: bool = False,
            limit: Optional[int] = None,
            timeout: Timeout = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            **kwargs,
    ) -> JSONDict:
        """
        Call list-like API methods with optimized pagination and retries.

        Args:
            api_method: API method name, e.g. crm.deal.list.
            params: API method parameters.
            descending: Whether to sort in descending order.
            limit: Maximum number of items to return.
            timeout: Request timeout in seconds.
            prefer_version: Preferred API version to resolve the method against.

        Returns:
            API response payload.
        """
        return self._call_with_retries(
            call_func=call_list_fast,
            parameters=dict(
                api_method=api_method,
                params=params,
                descending=descending,
                limit=limit,
                timeout=timeout,
                prefer_version=prefer_version,
                **kwargs,
            ),
        )


class AbstractBitrixTokenLocal(AbstractBitrixToken):
    """Token wrapper bound to a local Bitrix app."""

    bitrix_app: "AbstractBitrixAppLocal" = NotImplemented
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
    """Concrete token wrapper for OAuth or webhook tokens."""

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            refresh_token: Optional[Text] = None,
            expires: Optional[datetime] = None,
            expires_in: Optional[int] = None,
            bitrix_app: Optional["AbstractBitrixApp"] = None,
    ):
        """
        Initialize a token bound to a specific Bitrix portal.

        Args:
            domain: Portal domain, for example ``example.bitrix24.com``.
            auth_token: OAuth access token or webhook token string.
            refresh_token: OAuth refresh token.
            expires: OAuth access token expiration datetime.
            expires_in: OAuth access token lifetime in seconds.
            bitrix_app: Bitrix app used to refresh OAuth tokens.
        """
        self.domain = domain
        self.auth_token = auth_token
        self.refresh_token = refresh_token
        self.expires = expires
        self.expires_in = expires_in
        self.bitrix_app = bitrix_app

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
            expires=oauth_token.expires,
            expires_in=oauth_token.expires_in,
            bitrix_app=bitrix_app,
        )

    @classmethod
    def from_oauth(
            cls,
            oauth: "OAuth",
            bitrix_app: "AbstractBitrixApp",
    ) -> "BitrixToken":
        """"""
        oauth_token = oauth.oauth_token
        return cls(
            domain=oauth.portal_domain,
            auth_token=oauth_token.access_token,
            refresh_token=oauth_token.refresh_token,
            expires=oauth_token.expires,
            expires_in=oauth_token.expires_in,
            bitrix_app=bitrix_app,
        )

    @classmethod
    def from_oauth_event_data(
            cls,
            oauth_event_data: "OAuthEventData",
            bitrix_app: "AbstractBitrixApp",
    ) -> "BitrixToken":
        """"""

        auth = oauth_event_data.auth

        if auth.oauth_token is None:
            raise ValueError("Event auth data does not contain OAuth token")

        return cls.from_oauth(oauth=auth, bitrix_app=bitrix_app)

    @classmethod
    def from_oauth_workflow_data(
            cls,
            oauth_workflow_data: "OAuthWorkflowData",
            bitrix_app: "AbstractBitrixApp",
    ) -> "BitrixToken":
        """"""
        return cls.from_oauth(oauth=oauth_workflow_data.auth, bitrix_app=bitrix_app)


class BitrixTokenLocal(AbstractBitrixTokenLocal):
    """Token wrapper for local Bitrix apps without explicit domain."""

    def __init__(
            self,
            *,
            auth_token: Text,
            refresh_token: Optional[Text] = None,
            expires: Optional[datetime] = None,
            expires_in: Optional[int] = None,
            bitrix_app: "AbstractBitrixAppLocal",
    ):
        """
        Initialize a token for local Bitrix app context.

        Args:
            auth_token: OAuth access token.
            refresh_token: OAuth refresh token.
            expires: OAuth access token expiration datetime.
            expires_in: OAuth access token lifetime in seconds.
            bitrix_app: Local Bitrix app bound to the current portal.
        """
        self.auth_token = auth_token
        self.refresh_token = refresh_token
        self.expires = expires
        self.expires_in = expires_in
        self.bitrix_app = bitrix_app

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
            expires=oauth_token.expires,
            expires_in=oauth_token.expires_in,
            bitrix_app=bitrix_app,
        )

    @classmethod
    def from_oauth(
            cls,
            oauth: "OAuth",
            bitrix_app: "AbstractBitrixAppLocal",
    ) -> "BitrixTokenLocal":
        """"""
        oauth_token = oauth.oauth_token
        return cls(
            auth_token=oauth_token.access_token,
            refresh_token=oauth_token.refresh_token,
            expires=oauth_token.expires,
            expires_in=oauth_token.expires_in,
            bitrix_app=bitrix_app,
        )

    @classmethod
    def from_oauth_event_data(
            cls,
            oauth_event_data: "OAuthEventData",
            bitrix_app: "AbstractBitrixAppLocal",
    ) -> "BitrixTokenLocal":
        """"""

        auth = oauth_event_data.auth

        if auth.oauth_token is None:
            raise ValueError("Event auth data does not contain OAuth token")

        return cls.from_oauth(oauth=auth, bitrix_app=bitrix_app)

    @classmethod
    def from_oauth_workflow_data(
            cls,
            oauth_workflow_data: "OAuthWorkflowData",
            bitrix_app: "AbstractBitrixAppLocal",
    ) -> "BitrixTokenLocal":
        """"""
        return cls.from_oauth(oauth=oauth_workflow_data.auth, bitrix_app=bitrix_app)


class BitrixWebhook(BitrixToken):
    """Token wrapper for webhook auth tokens."""

    __AUTH_TOKEN_PARTS_COUNT: Final[int] = 2

    def __init__(
            self,
            *,
            domain: Text,
            webhook_token: Text,
    ):
        """
        Initialize a webhook token wrapper.

        Args:
            domain: Portal domain, for example ``example.bitrix24.com``.
            webhook_token: Webhook token in ``user_id/webhook_key`` format.
        """
        super().__init__(domain=domain, auth_token=self._normalize_token(webhook_token))

    @classmethod
    def _normalize_token(cls, webhook_token: Text) -> Text:
        """Validate and normalize webhook token to ``user_id/webhook_key`` format."""

        parts = webhook_token.strip("/").split("/")

        if len(parts) != cls.__AUTH_TOKEN_PARTS_COUNT:
            raise ValueError(
                f"Invalid webhook token format: "
                f"expected 'user_id/webhook_key', got {webhook_token!r}",
            )

        user_id, webhook_key = parts

        if not user_id.isdigit():
            raise ValueError(
                f"Invalid webhook token format: "
                f"expected numeric user_id, got {user_id!r}",
            )

        if not webhook_key:
            raise ValueError("Invalid webhook token format: webhook_key is empty")

        return f"{int(user_id)}/{webhook_key}"

    @property
    def user_id(self) -> int:
        """Return the webhook user_id parsed from auth_token."""
        user_id_str, _ = self.auth_token.split("/", maxsplit=1)
        return int(user_id_str)

    @property
    def webhook_key(self) -> Text:
        """Return the webhook key parsed from auth_token."""
        _, webhook_key = self.auth_token.split("/", maxsplit=1)
        return webhook_key
