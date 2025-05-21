from abc import ABC
from typing import Text, TYPE_CHECKING

from ..bitrix_api import BitrixToken
from ..utils.functional import Classproperty

if TYPE_CHECKING:
    from .. import Client


class Scope(ABC):
    """"""

    __slots__ = ("_client",)

    _client: "Client"

    def __init__(self, client: "Client"):
        self._client = client

    @Classproperty
    def name(cls) -> Text:
        return cls.__name__.lower()

    @property
    def bitrix_token(self) -> BitrixToken:
        return self._client.bitrix_token
