from abc import ABC, abstractmethod
from typing import Optional, Text, Union, Dict, Iterable

from ..utils.types import B24BatchRequestData, JSONDict

from .functions import api_call
from .functions.batch_api_call import batch_api_call


class BaseBitrixToken(ABC):
    """"""

    DEFAULT_TIMEOUT: int = 10

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

    def call_api_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            *,
            timeout: Union[int, float, None] = DEFAULT_TIMEOUT,
    ) -> JSONDict:
        """"""
        return api_call(
            domain=self.domain,
            api_method=api_method,
            auth_token=self.auth_token,
            is_webhook=self.is_webhook,
            params=params,
            timeout=timeout,
        )

    def batch_api_call(
            self,
            methods: Union[Dict[Text, B24BatchRequestData], Iterable[B24BatchRequestData]],
            *,
            halt: int = 0,
            chunk_size: int = 50,
            timeout: int = DEFAULT_TIMEOUT,
    ):
        return batch_api_call(
            methods=methods,
            domain=self.domain,
            auth_token=self.auth_token,
            halt=halt,
            chunk_size=chunk_size,
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
