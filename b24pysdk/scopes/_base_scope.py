from abc import ABC
from typing import TYPE_CHECKING

from ._base_context import BaseContext

if TYPE_CHECKING:
    from .. import Client


class BaseScope(BaseContext, ABC):
    """"""

    __slots__ = ("_client",)

    _client: "Client"

    def __init__(self, client: "Client"):
        self._client = client

    def __repr__(self):
        return f"scopes.{self.__class__.__name__}(client={self._client})"

    @property
    def _context(self) -> "Client":
        """"""
        return self._client
