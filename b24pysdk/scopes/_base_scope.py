from abc import ABC
from typing import TYPE_CHECKING

from ._base_context import BaseContext

if TYPE_CHECKING:
    from ..client import BaseClient


class BaseScope(BaseContext, ABC):
    """"""

    __slots__ = ("_client",)

    _client: "BaseClient"

    def __init__(self, client: "BaseClient"):
        self._client = client

    def __repr__(self):
        return f"scopes.{self.__class__.__name__}(client={self._client})"

    @property
    def _context(self) -> "BaseClient":
        """"""
        return self._client
