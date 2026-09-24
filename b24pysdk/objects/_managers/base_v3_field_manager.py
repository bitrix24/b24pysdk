from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Dict, Generic, Text

from ...constants.version import B24APIVersion
from ...schemas.v3 import V3Field, V3FieldData
from ...utils.type_vars import BOT
from ...utils.types import JSONList, Timeout
from ..errors import BitrixObjectClientError
from .base_field_manager import BaseFieldManager

if TYPE_CHECKING:
    from ...api.requests import BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ...client import ClientV3

__all__ = [
    "BaseV3FieldManager",
]


class BaseV3FieldManager(BaseFieldManager[BOT], ABC, Generic[BOT]):
    """Manager for the standard REST API v3 ``field.get`` and ``field.list`` methods."""

    @property
    def _client(self) -> "ClientV3":
        """Return the configured API v3 client."""

        client = super()._client

        if client.VERSION != B24APIVersion.V3:
            raise BitrixObjectClientError(
                f"{self.__class__.__name__} requires a Bitrix24 API v3 client. "
                "Create it with Client(..., prefer_version=3).",
            )

        return client

    def list(self, *, timeout: Timeout = None) -> Dict[Text, V3Field]:
        """Return all field descriptions indexed by their Bitrix24 names."""

        fields = self._get_list_api_wrapper(self._client)(timeout=timeout).values

        return {
            field.name: field
            for field in fields
        }

    def get(
            self,
            attr_name: Text,
            *,
            timeout: Timeout = None,
    ) -> V3Field:
        """Return field metadata by SDK object attribute name."""

        bitrix_field = self._meta.get_field(attr_name)

        return self._get_api_wrapper(self._client)(
            name=bitrix_field.bitrix_code,
            timeout=timeout,
        ).value

    @abstractmethod
    def _get_api_wrapper(self, client: "ClientV3") -> Callable[..., "BitrixAPIValueRequest[V3FieldData, V3Field]"]:
        """Return the concrete REST API v3 ``field.get`` wrapper."""
        raise NotImplementedError

    @abstractmethod
    def _get_list_api_wrapper(self, client: "ClientV3") -> Callable[..., "BitrixAPIValuesRequest[JSONList, V3Field]"]:
        """Return the concrete REST API v3 ``field.list`` wrapper."""
        raise NotImplementedError
