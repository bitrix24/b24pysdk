from abc import ABC
from typing import TYPE_CHECKING, Text

from ..bitrix_api.bitrix_token import AbstractBitrixToken
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
    def bitrix_token(self) -> AbstractBitrixToken:
        return self._client.bitrix_token
