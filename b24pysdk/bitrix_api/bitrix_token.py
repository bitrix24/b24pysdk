from abc import ABC, abstractmethod
from typing import Dict, Optional, Sequence, Text, Union

from ..utils.types import B24BatchRequestData, JSONDict, Key, Timeout

from .functions import call_method, call_batch, call_batches


class BaseBitrixToken(ABC):
    """"""

    domain: Text = NotImplemented
    """"""

    auth_token: Text = NotImplemented
    """"""

    is_webhook: bool = NotImplemented
    """"""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

    def call_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            *,
            timeout: Timeout = None,
    ) -> JSONDict:
        """"""
        return call_method(
            domain=self.domain,
            api_method=api_method,
            auth_token=self.auth_token,
            is_webhook=self.is_webhook,
            params=params,
            timeout=timeout,
        )

    def call_batch(
            self,
            methods: Union[Dict[Key, B24BatchRequestData], Sequence[B24BatchRequestData]],
            *,
            halt: bool = False,
            ignore_size_limit: bool = False,
            timeout: Timeout = None,
    ) -> JSONDict:
        """"""
        return call_batch(
            methods=methods,
            domain=self.domain,
            auth_token=self.auth_token,
            halt=halt,
            is_webhook=self.is_webhook,
            ignore_size_limit=ignore_size_limit,
            timeout=timeout,
        )

    def call_batches(
            self,
            methods: Union[Dict[Key, B24BatchRequestData], Sequence[B24BatchRequestData]],
            *,
            halt: bool = False,
            timeout: Timeout = None,
    ) -> JSONDict:
        """"""
        return call_batches(
            methods=methods,
            domain=self.domain,
            auth_token=self.auth_token,
            halt=halt,
            is_webhook=self.is_webhook,
            timeout=timeout,
        )


class BitrixToken(BaseBitrixToken):
    """"""

    def __init__(
            self,
            domain: Text,
            auth_token: Text,
            is_webhook: bool = False,
    ):
        self.domain = domain
        self.auth_token = auth_token
        self.is_webhook = is_webhook
