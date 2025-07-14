from abc import ABC
from typing import Callable, Optional, Text

from ..bitrix_api.classes import BitrixAPIRequest
from ..utils.functional import Classproperty
from .scope import Scope


class Base(ABC):
    """"""

    __slots__ = ("_scope", "_path")

    _scope: Scope
    _path: Text

    def __init__(self, scope: Scope):
        self._scope = scope
        self._path = self._get_path()

    def _fields(self, *args, **kwargs) -> BitrixAPIRequest:
        raise NotImplementedError(f"Method 'fields' is not implemented in class '{self.__class__.__name__}'")

    def _add(self, *args, **kwargs) -> BitrixAPIRequest:
        raise NotImplementedError(f"Method 'add' is not implemented in class '{self.__class__.__name__}'")

    def _get(self, *args, **kwargs) -> BitrixAPIRequest:
        raise NotImplementedError(f"Method 'get' is not implemented in class '{self.__class__.__name__}'")

    def _list(self, *args, **kwargs) -> BitrixAPIRequest:
        raise NotImplementedError(f"Method 'list' is not implemented in class '{self.__class__.__name__}'")

    def _update(self, *args, **kwargs) -> BitrixAPIRequest:
        raise NotImplementedError(f"Method 'update' is not implemented in class '{self.__class__.__name__}'")

    def _delete(self, *args, **kwargs) -> BitrixAPIRequest:
        raise NotImplementedError(f"Method 'delete' is not implemented in class '{self.__class__.__name__}'")

    @Classproperty
    def _bitrix_entity(cls) -> Text:
        """"""
        return cls.__name__.lower()

    def _get_path(self, base: Optional["Base"] = None) -> Text:
        """"""
        return f"{getattr(base, '_path', self._scope.name)}.{self._bitrix_entity}"

    def _get_api_method(self, method: Callable) -> Text:
        """"""
        return f"{self._path}.{self.__to_camel_case(method.__name__.strip('_'))}"

    @staticmethod
    def __to_camel_case(snake_str: Text) -> Text:
        """Converts Python methods names to camelCase to be used in _get_api_method"""
        first, *parts = snake_str.split("_")
        return "".join([first.lower(), *(str.title(part) for part in parts)])
