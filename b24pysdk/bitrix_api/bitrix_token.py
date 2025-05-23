from abc import ABC, abstractmethod
from typing import Optional, Text, Union

from ..utils.types import JSONDict

from .functions import api_call


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
