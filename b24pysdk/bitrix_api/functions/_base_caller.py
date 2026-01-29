from abc import ABC, abstractmethod
from typing import Optional, Text

from ..._config import Config
from ...protocols import BitrixTokenProtocol
from ...utils.types import JSONDict

__all__ = [
    "BaseCaller",
]


class BaseCaller(ABC):
    """"""

    __slots__ = (
        "_api_method",
        "_auth_token",
        "_bitrix_token",
        "_config",
        "_domain",
        "_is_webhook",
        "_kwargs",
        "_params",
    )

    _config: Config
    _domain: Text
    _auth_token: Text
    _is_webhook: bool
    _api_method: Text
    _params: JSONDict
    _bitrix_token: Optional[BitrixTokenProtocol]
    _kwargs: JSONDict

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            api_method: Text,
            params: Optional[JSONDict] = None,
            bitrix_token: Optional[BitrixTokenProtocol] = None,
            **kwargs,
    ):
        self._config = Config()
        self._domain = domain
        self._auth_token = auth_token
        self._is_webhook = is_webhook
        self._api_method = api_method
        self._params = params or dict()
        self._bitrix_token = bitrix_token
        self._kwargs = kwargs

    @abstractmethod
    def call(self) -> JSONDict:
        """"""
        raise NotImplementedError
