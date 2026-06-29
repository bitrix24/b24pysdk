from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Text

from ...protocols import BitrixTokenFullProtocol
from ...utils.type_vars import ResponseT
from ...utils.types import B24RequestTuple, JSONDict

__all__ = [
    "AbstractBitrixAPIRequest",
]


class AbstractBitrixAPIRequest(ABC, Generic[ResponseT]):
    """
    Base class for lazy Bitrix24 API request objects.

    Stores request parameters, executes the API call through a Bitrix token,
    converts the raw JSON response into a typed response object, and caches the
    converted response after the first access.
    """

    __slots__ = ("_api_method", "_bitrix_token", "_kwargs", "_params", "_response")

    _bitrix_token: BitrixTokenFullProtocol
    _api_method: Text
    _params: Optional[JSONDict]
    _kwargs: JSONDict
    _response: Optional[ResponseT]

    def __init__(
            self,
            *,
            bitrix_token: BitrixTokenFullProtocol,
            api_method: Text,
            params: Optional[JSONDict] = None,
            **kwargs: JSONDict,
    ):
        """
        Initialize a lazy API request.

        Args:
            bitrix_token: Token-like object used to execute Bitrix24 API calls.
            api_method: Bitrix24 REST API method name.
            params: Optional request parameters.
            **kwargs: Extra options forwarded to the token call.
        """
        self._bitrix_token = bitrix_token
        self._api_method = api_method
        self._params = params
        self._kwargs = kwargs
        self._response = None

    def __str__(self):
        return f"<{self.__class__.__name__} {self._api_method}({self._param_string})>"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"api_method='{self._api_method}', "
            f"params={self._params})"
        )

    @property
    def _param_string(self) -> Optional[Text]:
        """
        Return request parameters formatted for human-readable representation.

        Returns:
            Comma-separated ``key=value`` string for mapping parameters,
            otherwise ``None``.
        """
        if isinstance(self._params, dict):
            return ", ".join(f"{key}={value}" for key, value in self._params.items())
        else:
            return None

    @property
    def _as_tuple(self) -> B24RequestTuple:
        """
        Return request as a batch-compatible tuple.

        Returns:
            Tuple containing API method name and request parameters.
        """
        return self._api_method, self._params

    @property
    def response(self) -> ResponseT:
        """
        Return cached response or execute the request once.

        The response is fetched lazily on first access and then reused.
        """
        if self._response is None:
            return self._get_and_set_response()
        return self._response

    def _call(self) -> Any:
        """
        Execute the raw Bitrix24 API call.

        Returns:
            Raw JSON response returned by the token.
        """
        return self._bitrix_token.call_method(
            api_method=self._api_method,
            params=self._params,
            **self._kwargs,
        )

    @abstractmethod
    def _convert_response(self, json_response: Any) -> ResponseT:
        """
        Convert raw JSON response into a typed response object.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Converted response object.
        """
        raise NotImplementedError

    def _get_and_set_response(self) -> ResponseT:
        """
        Execute the request, convert response, and cache it.

        Returns:
            Converted response object.
        """
        self._response = self._convert_response(self._call())
        return self._response

    def call(self) -> ResponseT:
        """
        Execute the request immediately.

        Unlike ``response``, this method always performs a new API call and
        replaces the cached response with the latest converted result.

        Returns:
            Converted response object.
        """
        return self._get_and_set_response()
