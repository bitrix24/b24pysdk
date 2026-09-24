from abc import ABC
from typing import TYPE_CHECKING, Generic

from ....constants.version import B24APIVersion
from ....utils.type_vars import BOT
from ...errors import BitrixObjectClientError
from .base_object_manager import BaseObjectManager

if TYPE_CHECKING:
    from ....client import ClientV3

__all__ = [
    "BaseV3ObjectManager",
]


class BaseV3ObjectManager(BaseObjectManager[BOT], ABC, Generic[BOT]):
    """Base query manager for objects backed by Bitrix24 REST API v3."""

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
