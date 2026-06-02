from abc import ABC
from typing import TYPE_CHECKING

from ._base_context import BaseContext

if TYPE_CHECKING:
    from ..client import BaseClient


class BaseScope(BaseContext, ABC):
    """
    Base class for root Bitrix24 API scopes.

    A scope is a top-level API namespace attached directly to the SDK client.
    It inherits token access, requester options, and API method path generation
    from ``BaseContext``.
    """

    __slots__ = ("_client",)

    _client: "BaseClient"

    def __init__(self, client: "BaseClient"):
        """
        Initialize a scope with the root client.

        Args:
            client: SDK client that owns this scope.
        """
        self._client = client

    def __repr__(self):
        return f"scopes.{self.__class__.__name__}(client={self._client})"

    @property
    def _context(self) -> "BaseClient":
        """
        Return the root SDK client used as this scope context.

        Returns:
            Client from which token, requester options, and root API path are
            inherited.
        """
        return self._client
