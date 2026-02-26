from abc import ABC, abstractmethod
from typing import Optional, Text, Union

from ..._config import Config
from ...constants.version import B24APIVersion
from ...protocols import BitrixTokenProtocol
from ...utils.types import B24APIVersionLiteral, JSONDict

__all__ = [
    "BaseCaller",
]


class BaseCaller(ABC):
    """"""

    __slots__ = (
        "_api_method",
        "_api_version",
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
    _api_version: B24APIVersion
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
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            bitrix_token: Optional[BitrixTokenProtocol] = None,
            **kwargs,
    ):
        self._config = Config()
        self._domain = domain
        self._auth_token = auth_token
        self._is_webhook = is_webhook
        self._api_method = api_method
        self._params = params or {}
        self._api_version = self._resolve_api_version(api_method, prefer_version)
        self._bitrix_token = bitrix_token
        self._kwargs = kwargs

    def _resolve_api_version(
            self,
            api_method: Text,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> B24APIVersion:
        """"""
        if prefer_version == B24APIVersion.V3 and self._config.is_api_v3_method(api_method):
            return B24APIVersion.V3
        else:
            return B24APIVersion.V2

    @abstractmethod
    def call(self) -> JSONDict:
        """"""
        raise NotImplementedError
