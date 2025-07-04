from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional, Sequence, Text, Tuple, Union

from ..error import BitrixAPIExpiredToken
from ..utils.types import B24BatchRequestData, JSONDict, Key, Timeout
from .bitrix_app import BitrixApp
from .functions import call_batch, call_batches, call_method
from .oauth_requester import OAuthRequester


class AbstractBitrixToken(ABC):
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

    def _call_with_refresh(
            self,
            call_func: Callable,
            parameters: Dict,
            auto_refresh: bool = True,
    ) -> JSONDict:
        """"""
        try:
            return call_func(**self._auth_data, **parameters)
        except BitrixAPIExpiredToken as error:
            if auto_refresh and not self.is_webhook:
                self.auth_token, self.refresh_token = self.refresh()
                return call_func(**self._auth_data, **parameters)
            else:
                raise error

    def refresh(self) -> Tuple[Text, Text]:
        """"""
        json_response = self.oauth_requester.refresh(refresh_token=self.refresh_token)
        return json_response["access_token"], json_response["refresh_token"]

    def call_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            *,
            auto_refresh: bool = True,
            timeout: Timeout = None,
    ) -> JSONDict:
        """"""
        return self._call_with_refresh(
            call_func=call_method,
            parameters=dict(
                api_method=api_method,
                params=params,
                timeout=timeout,
            ),
            auto_refresh=auto_refresh,
        )

    def call_batch(
            self,
            methods: Union[Dict[Key, B24BatchRequestData], Sequence[B24BatchRequestData]],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            auto_refresh: bool = True,
            timeout: Timeout = None,
    ) -> JSONDict:
        """"""
        return self._call_with_refresh(
            call_func=call_batch,
            parameters=dict(
                methods=methods,
                halt=halt,
                ignore_size_limit=ignore_size_limit,
                timeout=timeout,
            ),
            auto_refresh=auto_refresh,
        )

    def call_batches(
            self,
            methods: Union[Dict[Key, B24BatchRequestData], Sequence[B24BatchRequestData]],
            *,
            halt: bool = False,
            auto_refresh: bool = True,
            timeout: Timeout = None,
    ) -> JSONDict:
        """"""
        return self._call_with_refresh(
            call_func=call_batches,
            parameters=dict(
                methods=methods,
                halt=halt,
                timeout=timeout,
            ),
            auto_refresh=auto_refresh,
        )


class BitrixToken(AbstractBitrixToken):
    """"""

    def __init__(
            self,
            domain: Text,
            auth_token: Text,
            refresh_token: Optional[Text] = None,
            bitrix_app: Optional[BitrixApp] = None,
    ):
        self.domain = domain
        self.auth_token = auth_token
        self.refresh_token = refresh_token
        self.bitrix_app = bitrix_app


class BitrixWebhook(BitrixToken):
    """"""

    def __init__(
            self,
            domain: Text,
            auth_token: Text,
    ):
        super().__init__(domain, auth_token)
