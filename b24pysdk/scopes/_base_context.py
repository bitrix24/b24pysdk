from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Optional, Text, Type, TypeVar, Union

from ..api.requests import AbstractBitrixAPIRequest, BitrixAPIRequest
from ..protocols import BitrixTokenFullProtocol
from ..utils.functional import classproperty
from ..utils.types import JSONDict, Timeout

if TYPE_CHECKING:
    from ..client import BaseClient


_BARQT = TypeVar("_BARQT", bound=AbstractBitrixAPIRequest)


class BaseContext(ABC):
    """"""

    __slots__ = ()

    def __str__(self):
        return self._path

    # noinspection PyMethodParameters
    @classproperty
    def _name(cls) -> Text:
        return cls.__name__.lower()

    @property
    @abstractmethod
    def _context(self) -> Union["BaseContext", "BaseClient"]:
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
        return "".join((first.lower(), *(part.title() for part in parts)))

    def _get_api_method(self, api_wrapper: Callable[..., _BARQT]) -> Text:
        """"""
        api_wrapper_name = getattr(api_wrapper, "__name__", None)
        return f"{self}.{self.__to_camel_case(api_wrapper_name.strip('_'))}" if api_wrapper_name else str(self)

    def _make_bitrix_api_request(
            self,
            api_wrapper: Callable[..., _BARQT],
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            bitrix_api_request_type: Type[_BARQT] = BitrixAPIRequest,
            **kwargs,
    ) -> _BARQT:
        """"""

        kwargs = self._kwargs | kwargs

        if timeout:
            kwargs["timeout"] = timeout

        return bitrix_api_request_type(
            bitrix_token=self._bitrix_token,
            api_method=self._get_api_method(api_wrapper),
            params=params,
            **kwargs,
        )
