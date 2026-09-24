from abc import ABC
from typing import TYPE_CHECKING, Dict, Generic, Text

from ..constants.version import B24APIVersion
from ..schemas.v3 import V3Field
from ..utils.type_vars import BOPKT
from ..utils.types import Timeout
from ._base_object import BaseObject
from .errors import BitrixObjectClientError

if TYPE_CHECKING:
    from ..client import ClientV3

__all__ = [
    "BaseV3Object",
]


class BaseV3Object(BaseObject[BOPKT], ABC, Generic[BOPKT]):
    """Base class for SDK objects backed by Bitrix24 REST API v3."""

    @property
    def client(self) -> "ClientV3":
        """Return the configured API v3 client."""

        client = super().client

        if client.VERSION != B24APIVersion.V3:
            raise BitrixObjectClientError(
                f"{self.__class__.__name__} requires a Bitrix24 API v3 client. "
                "Create it with Client(..., prefer_version=3).",
            )

        return client

    def get_fields(self, *, timeout: Timeout = None) -> Dict[Text, V3Field]:
        """Return API v3 field descriptions cached by the current client."""
        return super().get_fields(timeout=timeout)

    def get_field(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> V3Field:
        """Return an API v3 field description by its Bitrix24 name."""
        return super().get_field(bitrix_code, timeout=timeout)

    def get_field_title(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> Text:
        """Return the localized title of an API v3 field."""
        return self.get_field(bitrix_code, timeout=timeout).title
