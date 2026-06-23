from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Optional, Text, Type, Union, overload

from ..api.requests import BitrixAPIRequest
from ..protocols import BitrixTokenFullProtocol
from ..utils.functional import classproperty
from ..utils.type_vars import BARequestT, BAResultT, BAValueT
from ..utils.types import JSONDict, Timeout

if TYPE_CHECKING:
    from ..client import BaseClient

__all__ = [
    "BaseContext",
]


class BaseContext(ABC):
    """
    Base class for SDK API contexts.

    A context represents a namespace in the Bitrix24 REST API method tree.
    It builds dotted API method paths from nested context objects and creates
    lazy request objects bound to the current client token and requester options.
    """

    __slots__ = ()

    def __str__(self):
        return self._path

    # noinspection PyMethodParameters
    @classproperty
    def _name(cls) -> Text:
        """
        Return context name used in API method paths.

        By default, the lower-cased class name is used as the path segment.

        Returns:
            Context path segment.
        """
        return cls.__name__.lower()

    @property
    @abstractmethod
    def _context(self) -> Union["BaseContext", "BaseClient"]:
        """
        Return parent context or client.

        Concrete context classes must provide the object from which token,
        requester options, and parent path are inherited.

        Returns:
            Parent context or root client.
        """
        raise NotImplementedError

    @property
    def _bitrix_token(self) -> BitrixTokenFullProtocol:
        """
        Return Bitrix token inherited from the parent context.

        Returns:
            Token-like object used to execute API calls.
        """
        return getattr(self._context, "_bitrix_token")

    @property
    def _kwargs(self) -> JSONDict:
        """
        Return requester options inherited from the parent context.

        Returns:
            Dictionary of options forwarded to API request execution.
        """
        return getattr(self._context, "_kwargs")

    @property
    def _path(self) -> Text:
        """
        Build dotted API context path.

        Returns:
            Full context path assembled from parent path and current context
            name, for example ``crm.deal``.
        """
        base_path = getattr(self._context, "_path", None)
        return f"{base_path}.{self._name}" if base_path else self._name

    @staticmethod
    def __to_camel_case(snake_str: Text) -> Text:
        """
        Convert snake_case name to lowerCamelCase.

        Used to transform Python wrapper method names into Bitrix24 REST method
        segments.

        Args:
            snake_str: Python-style snake_case name.

        Returns:
            lowerCamelCase representation.
        """
        first, *parts = snake_str.split("_")
        return "".join((first.lower(), *(part.title() for part in parts)))

    def _get_api_method(self, api_wrapper: Callable[..., BARequestT]) -> Text:
        """
        Build Bitrix24 REST API method name for a wrapper method.

        Args:
            api_wrapper: Wrapper method used to infer the final method segment.

        Returns:
            Full Bitrix24 REST API method name.
        """
        api_wrapper_name = getattr(api_wrapper, "__name__", None)
        return f"{self}.{self.__to_camel_case(api_wrapper_name.strip('_'))}" if api_wrapper_name else str(self)

    @overload
    def _make_bitrix_api_request(
            self,
            api_wrapper: Callable[..., BARequestT],
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            *,
            bitrix_api_request_type: Type[BARequestT] = BitrixAPIRequest,
            result_adapter: None = None,
            **kwargs,
    ) -> BARequestT: ...

    @overload
    def _make_bitrix_api_request(
            self,
            api_wrapper: Callable[..., BARequestT],
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            *,
            bitrix_api_request_type: Type[BARequestT],
            result_adapter: Callable[[BAResultT], BAValueT],
            **kwargs,
    ) -> BARequestT: ...

    def _make_bitrix_api_request(
            self,
            api_wrapper: Callable[..., BARequestT],
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            *,
            bitrix_api_request_type: Type[BARequestT] = BitrixAPIRequest,
            result_adapter: Optional[Callable[[BAResultT], BAValueT]] = None,
            **kwargs,
    ) -> BARequestT:
        """
        Create a lazy Bitrix24 API request object.

        Args:
            api_wrapper: Wrapper method used to infer the API method name.
            params: Optional request parameters.
            timeout: Optional request timeout overriding inherited options.
            bitrix_api_request_type: Request class to instantiate.
            result_adapter: Optional callable that converts raw ``result`` to
                a Python-friendly value.
            **kwargs: Extra requester options overriding inherited options.

        Returns:
            Lazy request object bound to the current Bitrix token.
        """

        kwargs = self._kwargs | kwargs

        if timeout:
            kwargs["timeout"] = timeout

        if result_adapter:
            kwargs["result_adapter"] = result_adapter

        return bitrix_api_request_type(
            bitrix_token=self._bitrix_token,
            api_method=self._get_api_method(api_wrapper),
            params=params,
            **kwargs,
        )
