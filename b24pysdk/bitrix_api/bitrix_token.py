from abc import ABC, abstractmethod
from typing import Callable, Dict, Final, Mapping, Optional, Sequence, Text, Union, overload

from ..error import BitrixAPIExpiredToken
from ..utils.types import B24BatchRequestData, JSONDict, Key, Timeout
from .bitrix_app import BitrixApp, BitrixAppLocal
from .functions.call_batch import call_batch
from .functions.call_batches import call_batches
from .functions.call_list import call_list
from .functions.call_list_fast import call_list_fast
from .functions.call_method import call_method
from .requesters import OAuthRequester


class AbstractBitrixToken(ABC):
    """"""

    AUTO_REFRESH: bool = True
    """"""

    domain: Text = NotImplemented
    """"""

    auth_token: Text = NotImplemented
    """"""

    refresh_token: Text = NotImplemented
    """"""

    bitrix_app: Optional[BitrixApp] = NotImplemented
    """"""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"<{'Webhook' if self.is_webhook else 'Application'} token of portal {self.domain}>"

    @property
    def is_webhook(self) -> bool:
        """"""
        return not bool(self.bitrix_app)

    @property
    def oauth_requester(self) -> OAuthRequester:
        """"""
        return OAuthRequester(self.bitrix_app)

    @property
    def _auth_data(self) -> Dict:
        """"""
        return dict(
            domain=self.domain,
            auth_token=self.auth_token,
            is_webhook=self.is_webhook,
        )

    def _refresh_and_set(self):
        """"""
        json_response = self.refresh()
        self.auth_token, self.refresh_token = json_response["access_token"], json_response["refresh_token"]

    def _call_with_refresh(
            self,
            call_func: Callable,
            parameters: Dict,
    ) -> JSONDict:
        """"""
        try:
            return call_func(**self._auth_data, **parameters)
        except BitrixAPIExpiredToken:
            if self.AUTO_REFRESH and not self.is_webhook:
                self._refresh_and_set()
                return call_func(**self._auth_data, **parameters)
            else:
                raise

    def authorize(self, code: Text) -> JSONDict:
        """"""
        return self.oauth_requester.authorize(code=code)

    def refresh(self) -> JSONDict:
        """"""
        return self.oauth_requester.refresh(refresh_token=self.refresh_token)

    def call_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            *,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_refresh(
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
            methods: Mapping[Key, B24BatchRequestData],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        ...

    @overload
    def call_batch(
            self,
            methods: Sequence[B24BatchRequestData],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        ...

    def call_batch(
            self,
            methods: Union[Mapping[Key, B24BatchRequestData], Sequence[B24BatchRequestData]],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_refresh(
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
            methods: Mapping[Key, B24BatchRequestData],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        ...

    @overload
    def call_batches(
            self,
            methods: Sequence[B24BatchRequestData],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        ...

    def call_batches(
            self,
            methods: Union[Mapping[Key, B24BatchRequestData], Sequence[B24BatchRequestData]],
            *,
            halt: bool = False,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_refresh(
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
            limit: Optional[int] = None,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_refresh(
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
            descending: bool = False,
            limit: Optional[int] = None,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict:
        """"""
        return self._call_with_refresh(
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


class AbstractBitrixTokenLocal(AbstractBitrixToken, ABC):
    """"""

    bitrix_app: BitrixAppLocal = NotImplemented
    """"""

    @property
    def domain(self) -> Text:
        """"""
        return self.bitrix_app.domain


class BitrixToken(AbstractBitrixToken):
    """"""

    def __init__(
            self,
            domain: Text,
            auth_token: Text,
            *,
            refresh_token: Optional[Text] = None,
            bitrix_app: Optional[BitrixApp] = None,
    ):
        self.domain = domain
        self.auth_token = auth_token
        self.refresh_token = refresh_token
        self.bitrix_app = bitrix_app


class BitrixWebhook(BitrixToken):
    """"""

    __AUTH_TOKEN_PARTS_COUNT: Final[int] = 2

    def __init__(
            self,
            domain: Text,
            auth_token: Text,
    ):
        super().__init__(domain, auth_token)

    @property
    def user_id(self) -> int:
        """"""

        auth_parts = self.auth_token.strip("/").split("/")

        if len(auth_parts) == self.__AUTH_TOKEN_PARTS_COUNT and auth_parts[0].isdigit():
            return int(auth_parts[0])
        else:
            raise ValueError(f"Invalid webhook auth_token format: expected 'user_id/hook_key', got '{self.auth_token}'")

    @property
    def hook_key(self) -> Text:
        """"""

        auth_parts = self.auth_token.strip("/").split("/")

        if len(auth_parts) == self.__AUTH_TOKEN_PARTS_COUNT:
            return auth_parts[1]
        else:
            raise ValueError(f"Invalid webhook auth_token format: expected 'user_id/hook_key', got '{self.auth_token}'")
