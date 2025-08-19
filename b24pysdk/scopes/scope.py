from abc import ABC
from typing import TYPE_CHECKING, Callable, Optional, Text

from ..bitrix_api.bitrix_token import AbstractBitrixToken
from ..bitrix_api.classes import BitrixAPIRequest
from ..utils.functional import Classproperty
from ..utils.types import JSONDict, Timeout

if TYPE_CHECKING:
    from .. import Client


class Scope(ABC):
    """"""

    __slots__ = ("_client",)

    _client: "Client"

    def __init__(self, client: "Client"):
        self._client = client

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"scopes.{self.__class__.__name__}(client={self._client})"

    @Classproperty
    def _name(cls) -> Text:
        return cls.__name__.lower()

    @property
    def _bitrix_token(self) -> AbstractBitrixToken:
        return getattr(self._client, "_bitrix_token")

    @staticmethod
    def __to_camel_case(snake_str: Text) -> Text:
        """Converts Python methods names to camelCase to be used in _get_api_method"""
        first, *parts = snake_str.split("_")
        return "".join([first.lower(), *(part.title() for part in parts)])

    def _get_api_method(self, method: Callable) -> Text:
        """"""
        return f"{self}.{self.__to_camel_case(method.__name__.strip('_'))}"

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
        )
