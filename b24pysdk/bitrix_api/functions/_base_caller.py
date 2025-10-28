from abc import ABC, abstractmethod
from typing import Dict, Optional, Text

from ..._config import Config
from ...utils.types import JSONDict, Timeout
from ..protocols import BitrixTokenProtocol


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
        "_timeout",
    )

    _config: Config
    _domain: Text
    _auth_token: Text
    _is_webhook: bool
    _api_method: Text
    _params: JSONDict
    _timeout: Timeout
    _bitrix_token: Optional["BitrixTokenProtocol"]
    _kwargs: Dict

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            api_method: Text,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            bitrix_token: Optional["BitrixTokenProtocol"] = None,
            **kwargs,
    ):
        self._config = Config()
        self._domain = domain
        self._auth_token = auth_token
        self._is_webhook = is_webhook
        self._api_method = api_method
        self._params = params or dict()
        self._timeout = timeout
        self._bitrix_token = bitrix_token
        self._kwargs = kwargs

    @abstractmethod
    def call(self) -> JSONDict:
        """"""
        raise NotImplementedError
