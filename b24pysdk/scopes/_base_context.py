from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Optional, Text, Union

from ..bitrix_api.protocols import BitrixTokenFullProtocol
from ..bitrix_api.requests import BitrixAPIRequest
from ..utils.functional import Classproperty
from ..utils.types import JSONDict, Timeout

if TYPE_CHECKING:
    from .. import Client


class BaseContext(ABC):
    """"""

    __slots__ = ()

    def __str__(self):
        return self._path

    @Classproperty
    def _name(cls) -> Text:
        return cls.__name__.lower()

    @property
    @abstractmethod
    def _context(self) -> Union["BaseContext", "Client"]:
        """"""
        raise NotImplementedError

    @property
    def _bitrix_token(self) -> BitrixTokenFullProtocol:
        """"""
        return getattr(self._context, "_bitrix_token")

    @property
    def _kwargs(self) -> JSONDict:
        """"""
        return getattr(self._context, "_kwargs")

    @property
    def _path(self) -> Text:
        """"""
        base_path = getattr(self._context, "_path", None)
        return f"{base_path}.{self._name}" if base_path else self._name

    @staticmethod
    def __to_camel_case(snake_str: Text) -> Text:
        """Converts Python methods names to camelCase to be used in _get_api_method"""
        first, *parts = snake_str.split("_")
        return "".join([first.lower(), *(part.title() for part in parts)])

    def _get_api_method(self, api_wrapper: Callable) -> Text:
        """"""
        api_wrapper_name = getattr(api_wrapper, "__name__", None)
        return f"{self}.{self.__to_camel_case(api_wrapper_name.strip('_'))}" if api_wrapper_name else str(self)

    def _make_bitrix_api_request(
            self,
            api_wrapper: Callable,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if timeout:
            self._kwargs["timeout"] = timeout

        return BitrixAPIRequest(
            bitrix_token=self._bitrix_token,
            api_method=self._get_api_method(api_wrapper),
            params=params,
            **self._kwargs,
        )
