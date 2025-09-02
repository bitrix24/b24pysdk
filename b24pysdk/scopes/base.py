from abc import ABC
from typing import Callable, Dict, Optional, Text

from ..bitrix_api.bitrix_token import AbstractBitrixToken
from ..bitrix_api.classes import BitrixAPIRequest
from ..utils.functional import Classproperty
from ..utils.types import JSONDict, Timeout
from .scope import Scope


class Base(ABC):
    """"""

    __slots__ = ("_path", "_scope")

    _scope: Scope
    _path: Text

    def __init__(self, scope: Scope):
        self._scope = scope
        self._path = self._get_path()

    def __str__(self):
        return self._path

    def __repr__(self):
        return f"client.{self}"

    @Classproperty
    def _name(cls) -> Text:
        """"""
        return cls.__name__.lower()

    def _get_path(self, base: Optional["Base"] = None) -> Text:
        """"""
        return f"{getattr(base, '_path', self._scope)}.{self._name}"

    @property
    def _bitrix_token(self) -> AbstractBitrixToken:
        return getattr(self._scope, "_bitrix_token")

    @property
    def _kwargs(self) -> Dict:
        """"""
        return getattr(self._scope, "_kwargs")

    @staticmethod
    def __to_camel_case(snake_str: Text) -> Text:
        """Converts Python methods names to camelCase to be used in _get_api_method"""
        first, *parts = snake_str.split("_")
        return "".join([first.lower(), *(part.title() for part in parts)])

    def _get_api_method(self, method: Callable) -> Text:
        """"""
        if hasattr(method, "__name__"):
            return f"{self}.{self.__to_camel_case(method.__name__.strip('_'))}"
        else:
            return str(self)

    def _make_bitrix_api_request(
            self,
            api_method: Callable,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._bitrix_token,
            api_method=self._get_api_method(api_method),
            params=params,
            timeout=timeout,
            **self._kwargs,
        )
