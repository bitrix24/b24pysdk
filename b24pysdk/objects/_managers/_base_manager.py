from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Generic, Optional, Type, overload

from ...utils.type_vars import BOT
from ...utils.types import Self
from .._client_provider import ClientProvider
from ..errors import BitrixObjectError

if TYPE_CHECKING:
    from ...client import ClientType
    from .._object_metadata import ObjectMetadata

__all__ = [
    "BaseManager",
]


class BaseManager(ABC, Generic[BOT]):
    """Base descriptor for managers bound to an SDK object class."""

    __slots__ = ("_client_provider", "_object_class")

    _client_provider: ClientProvider
    _object_class: Optional[Type[BOT]]

    def __init__(
            self,
            *,
            object_class: Optional[Type[BOT]] = None,
            client_provider: Optional[ClientProvider] = None,
    ):
        self._object_class = object_class
        self._client_provider = client_provider or ClientProvider()

    def __get__(
            self,
            instance: None,
            owner: Type[BOT],
    ) -> Self:
        if instance is not None:
            raise AttributeError(f"{self.__class__.__name__} is available only on the object class.")

        return self._clone(
            object_class=owner,
            client_provider=self._client_provider,
        )

    @overload
    def using(self, *, client: "ClientType", client_factory: None = None) -> Self: ...

    @overload
    def using(self, *, client: None = None, client_factory: Callable[[], "ClientType"]) -> Self: ...

    def using(
            self,
            *,
            client: Optional["ClientType"] = None,
            client_factory: Optional[Callable[[], "ClientType"]] = None,
    ) -> Self:
        """Return a manager copy with an explicit client source."""

        if client is None and client_factory is None:
            raise ValueError("Pass either client or client_factory.")

        if client is not None and client_factory is not None:
            raise ValueError("Pass either client or client_factory, not both.")

        return self._clone(
            client_provider=ClientProvider(
                client=client,
                client_factory=client_factory,
            ),
        )

    @property
    def _client(self) -> "ClientType":
        """Return a concrete Bitrix24 client resolved through the client provider."""
        return self._client_provider.client

    def _get_object_class(self) -> Type[BOT]:
        """Return the SDK object class bound to this manager."""

        if self._object_class is None:
            raise BitrixObjectError(f"{self.__class__.__name__} is not bound to an object class.")

        return self._object_class

    @property
    def _meta(self) -> "ObjectMetadata[BOT]":
        """Return metadata of the SDK object class bound to this manager."""
        return self._get_object_class().get_meta()

    @abstractmethod
    def _clone(
            self,
            *,
            object_class: Optional[Type[BOT]] = None,
            client_provider: Optional[ClientProvider] = None,
    ) -> Self:
        """Return a manager copy with updated binding data."""
        raise NotImplementedError
