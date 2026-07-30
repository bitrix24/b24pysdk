import typing

from .._config import Config
from .errors import BitrixObjectClientError

if typing.TYPE_CHECKING:
    from ..client import ClientType

__all__ = [
    "ClientProvider",
]


class ClientProvider:
    """Lazy holder for a concrete Bitrix24 client or a client factory.

    ``client`` and ``client_factory`` are mutually exclusive. If neither is
    passed, the provider tries the SDK-level default client factory when the
    client is first requested.
    """

    __slots__ = ("_client", "_client_factory")

    _client: typing.Optional["ClientType"]
    _client_factory: typing.Optional[typing.Callable[[], "ClientType"]]

    def __init__(
            self,
            *,
            client: typing.Optional["ClientType"] = None,
            client_factory: typing.Optional[typing.Callable[[], "ClientType"]] = None,
    ):
        if client is not None and client_factory is not None:
            raise BitrixObjectClientError("Pass either client or client_factory, not both.")

        self._client = client
        self._client_factory = client_factory

    @property
    def client(self) -> "ClientType":
        """Return a concrete client, resolving factories lazily."""

        if self._client is not None:
            return self._client

        if self._client_factory is not None:
            self._client = self._client_factory()
            return self._client

        default_client_factory = Config().default_client_factory

        if default_client_factory is not None:
            self._client = default_client_factory()
            return self._client

        raise BitrixObjectClientError(
            "Bitrix client is not configured. Pass client, client_factory, "
            "or configure the SDK default client factory.",
        )
