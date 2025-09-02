from abc import ABC, abstractmethod
from typing import Dict, Optional, Text

from ...utils.types import JSONDict, Timeout


class BaseCaller(ABC):
    """"""

    __slots__ = (
        "_api_method",
        "_auth_token",
        "_domain",
        "_is_webhook",
        "_kwargs",
        "_params",
        "_timeout",
    )

    _domain: Text
    _auth_token: Text
    _is_webhook: bool
    _api_method: Text
    _params: JSONDict
    _timeout: Timeout
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
            **kwargs,
    ):
        self._domain = domain
        self._auth_token = auth_token
        self._is_webhook = is_webhook
        self._api_method = api_method
        self._params = params or dict()
        self._timeout = timeout
        self._kwargs = kwargs

    @abstractmethod
    def call(self) -> JSONDict:
        """"""
        raise NotImplementedError
