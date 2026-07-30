from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Text, Type

from ...utils.type_vars import BOT
from ...utils.types import Self, Timeout
from .._client_provider import ClientProvider
from ..errors import BitrixObjectFieldError
from ._base_manager import BaseManager

__all__ = [
    "BaseFieldManager",
]


class BaseFieldManager(BaseManager[BOT], ABC, Generic[BOT]):
    """Base descriptor for immediate Bitrix24 object field metadata access.

    The manager is declared on an SDK object class and is available only
    through that class. Concrete managers implement ``list()`` using the
    corresponding Bitrix24 API method. ``get()`` uses ``list()`` by default;
    specialized managers may override it when the API provides a dedicated
    field retrieval method.
    """

    __slots__ = ()

    @abstractmethod
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> Any:
        """Return all Bitrix24 field metadata immediately."""
        raise NotImplementedError

    def get(
            self,
            attr_name: Text,
            *,
            timeout: Timeout = None,
    ) -> Any:
        """Return field metadata by SDK object attribute name."""

        bitrix_field = self._meta.get_field(attr_name)

        try:
            return self.list(timeout=timeout)[bitrix_field.bitrix_code]
        except (KeyError, TypeError):
            raise BitrixObjectFieldError(
                f"{self._get_object_class().__name__} has no field metadata for attribute {attr_name!r}.",
            ) from None

    def _clone(
            self,
            *,
            object_class: Optional[Type[BOT]] = None,
            client_provider: Optional[ClientProvider] = None,
    ) -> Self:
        """Return a manager copy with updated binding data."""
        return self.__class__(
            object_class=self._object_class if object_class is None else object_class,
            client_provider=self._client_provider if client_provider is None else client_provider,
        )
