from abc import ABC
from typing import Callable, Generator, Generic, List, Optional, Text, Union

from ...protocols import BitrixTokenFullProtocol
from ...utils.type_vars import BAResultT, BAValueResponseT, BAValueT
from ...utils.types import JSONDict, JSONGenerator, JSONList
from ..responses import (
    BitrixAPIValueResponse,
    BitrixAPIValuesListFastResponse,
    BitrixAPIValuesListResponse,
    BitrixAPIValuesResponse,
)
from .bitrix_api_base_request import BitrixAPIBaseRequest

__all__ = [
    "BitrixAPIBaseValueRequest",
    "BitrixAPIValueRequest",
    "BitrixAPIValuesListFastRequest",
    "BitrixAPIValuesListRequest",
    "BitrixAPIValuesRequest",
]


class BitrixAPIBaseValueRequest(BitrixAPIBaseRequest[BAValueResponseT, BAResultT], ABC, Generic[BAValueResponseT, BAResultT, BAValueT]):
    """
    Base request for Python-friendly views over raw Bitrix24 ``result``.

    Subclasses expose adapted data through ``value`` or ``values`` while
    preserving the standard ``response`` and raw ``result`` contract.
    """

    __slots__ = ("_result_adapter",)

    _result_adapter: Callable[[BAResultT], Union[BAValueT, List[BAValueT], Generator[BAValueT, None, None]]]

    def __init__(
            self,
            *,
            bitrix_token: BitrixTokenFullProtocol,
            api_method: Text,
            params: Optional[JSONDict] = None,
            result_adapter: Callable[[BAResultT], Union[BAValueT, List[BAValueT], Generator[BAValueT, None, None]]],
            **kwargs: JSONDict,
    ):
        """
        Initialize a value request.

        Args:
            bitrix_token: Token-like object used to execute Bitrix24 API calls.
            api_method: Bitrix24 REST API method name.
            params: Optional request parameters.
            result_adapter: Callable converting raw Bitrix24 ``result`` to a
                Python-friendly value.
            **kwargs: Standard request arguments forwarded to the base request.
        """
        super().__init__(
            bitrix_token=bitrix_token,
            api_method=api_method,
            params=params,
            **kwargs,
        )
        self._result_adapter = result_adapter


class BitrixAPIValueRequest(BitrixAPIBaseValueRequest[BitrixAPIValueResponse[BAResultT, BAValueT], BAResultT, BAValueT], Generic[BAResultT, BAValueT]):
    """
    Lazy request object that exposes an adapted ``value``.

    ``result`` remains the raw Bitrix24 payload. ``value`` is produced from
    ``result`` by ``result_adapter`` and is intended for schemas or scalar
    Python-friendly values without lifecycle behavior.
    """

    __slots__ = ()

    @property
    def value(self) -> BAValueT:
        """
        Return adapted Python value from the response.

        Accessing this property may execute the request lazily on first access.
        """
        return self.response.value

    def _convert_response(self, json_response: JSONDict) -> BitrixAPIValueResponse[BAResultT, BAValueT]:
        """
        Convert raw JSON response into ``BitrixAPIValueResponse``.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed API response with adapted ``value`` access.
        """
        return BitrixAPIValueResponse.from_dict(json_response, result_adapter=self._result_adapter)


class BitrixAPIValuesRequest(BitrixAPIBaseValueRequest[BitrixAPIValuesResponse[BAResultT, BAValueT], BAResultT, List[BAValueT]], Generic[BAResultT, BAValueT]):
    """
    Lazy request object that exposes adapted ``values``.

    ``result`` remains the raw Bitrix24 payload. ``values`` is produced from
    ``result`` by ``result_adapter`` and is intended for list-like adapted
    collections without lifecycle behavior.
    """

    __slots__ = ()

    @property
    def values(self) -> List[BAValueT]:
        """
        Return adapted Python values from the response.

        Accessing this property may execute the request lazily on first access.
        """
        return self.response.values

    def as_list(
            self,
            limit: Optional[int] = None,
    ) -> "BitrixAPIValuesListRequest[BAValueT]":
        """
        Create a paginated list request from this values request.

        The returned request preserves the original values adapter and exposes
        both raw ``result`` and adapted ``values``.

        Args:
            limit: Optional maximum number of items to load.

        Returns:
            Adapted list request using the same API method, parameters, token,
            requester options, and result adapter.
        """
        return BitrixAPIValuesListRequest(
            bitrix_api_values_request=self,
            limit=limit,
            **self._kwargs,
        )

    def as_list_fast(
            self,
            descending: bool = False,
            limit: Optional[int] = None,
    ) -> "BitrixAPIValuesListFastRequest[BAValueT]":
        """
        Create a fast paginated list request from this values request.

        The returned request preserves the original values adapter and exposes
        both raw ``result`` and adapted ``values``.

        Args:
            descending: Whether to retrieve items in descending ID order.
            limit: Optional maximum number of items to retrieve.

        Returns:
            Adapted fast list request using ID-window pagination with the same
            API method, parameters, token, requester options, and result
            adapter.
        """
        return BitrixAPIValuesListFastRequest(
            bitrix_api_values_request=self,
            descending=descending,
            limit=limit,
            **self._kwargs,
        )

    def _convert_response(self, json_response: JSONDict) -> BitrixAPIValuesResponse[BAResultT, BAValueT]:
        """
        Convert raw JSON response into ``BitrixAPIValuesResponse``.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed API response with adapted ``values`` access.
        """
        return BitrixAPIValuesResponse.from_dict(json_response, result_adapter=self._result_adapter)


class BitrixAPIValuesListRequest(BitrixAPIBaseValueRequest[BitrixAPIValuesListResponse[BAValueT], JSONList, List[BAValueT]], Generic[BAValueT]):
    """
    Lazy list request that exposes adapted ``values``.

    This duplicates the standard list-request lifecycle for values requests to
    keep the existing ``BitrixAPIRequest.as_list()`` behavior unchanged.
    """

    __slots__ = ("_limit",)

    _limit: Optional[int]

    def __init__(
            self,
            *,
            bitrix_api_values_request: BitrixAPIValuesRequest[BAResultT, BAValueT],
            limit: Optional[int] = None,
            **kwargs: JSONDict,
    ):
        """
        Initialize an adapted list request from a values request.

        Args:
            bitrix_api_values_request: Source values request to convert into a
                list request.
            limit: Optional maximum number of items to retrieve.
            **kwargs: Extra options overriding or extending source request
                options.
        """
        super().__init__(
            bitrix_token=bitrix_api_values_request._bitrix_token,
            api_method=bitrix_api_values_request._api_method,
            params=bitrix_api_values_request._params,
            result_adapter=bitrix_api_values_request._result_adapter,
            **bitrix_api_values_request._kwargs | kwargs,
        )
        self._limit = limit

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"api_method='{self._api_method}', "
            f"params={self._params}, "
            f"limit={self._limit})"
        )

    @property
    def values(self) -> List[BAValueT]:
        """
        Return adapted Python values from the list response.

        Accessing this property may execute the request lazily on first access.
        """
        return self.response.values

    def _convert_response(self, json_response: JSONDict) -> BitrixAPIValuesListResponse[BAValueT]:
        """
        Convert raw JSON response into ``BitrixAPIValuesListResponse``.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed list response with adapted ``values`` access.
        """
        return BitrixAPIValuesListResponse.from_dict(json_response, result_adapter=self._result_adapter)

    def _call(self) -> JSONDict:
        """
        Execute the request using standard list pagination.

        Returns:
            Raw JSON response returned by ``call_list``.
        """
        return self._bitrix_token.call_list(
            api_method=self._api_method,
            params=self._params,
            limit=self._limit,
            **self._kwargs,
        )


class BitrixAPIValuesListFastRequest(BitrixAPIBaseValueRequest[BitrixAPIValuesListFastResponse[BAValueT], JSONGenerator, Generator[BAValueT, None, None]], Generic[BAValueT]):
    """
    Lazy fast list request that exposes adapted ``values``.

    This duplicates the fast list-request lifecycle for values requests to keep
    the existing ``BitrixAPIRequest.as_list_fast()`` behavior unchanged.
    """

    __slots__ = ("_descending", "_limit")

    _descending: bool
    _limit: Optional[int]

    def __init__(
            self,
            *,
            bitrix_api_values_request: BitrixAPIValuesRequest[BAResultT, BAValueT],
            descending: bool = False,
            limit: Optional[int] = None,
            **kwargs: JSONDict,
    ):
        """
        Initialize an adapted fast list request from a values request.

        Args:
            bitrix_api_values_request: Source values request to convert into a
                fast list request.
            descending: Whether to retrieve items in descending ID order.
            limit: Optional maximum number of items to retrieve.
            **kwargs: Extra options overriding or extending source request
                options.
        """
        super().__init__(
            bitrix_token=bitrix_api_values_request._bitrix_token,
            api_method=bitrix_api_values_request._api_method,
            params=bitrix_api_values_request._params,
            result_adapter=bitrix_api_values_request._result_adapter,
            **bitrix_api_values_request._kwargs | kwargs,
        )
        self._descending = descending
        self._limit = limit

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"api_method='{self._api_method}', "
            f"params={self._params}, "
            f"descending={self._descending}, "
            f"limit={self._limit})"
        )

    @property
    def values(self) -> Generator[BAValueT, None, None]:
        """
        Return adapted Python values from the fast list response.

        Accessing this property may execute the request lazily on first access.
        """
        return self.response.values

    def _convert_response(self, json_response: JSONDict) -> BitrixAPIValuesListFastResponse[BAValueT]:
        """
        Convert raw JSON response into ``BitrixAPIValuesListFastResponse``.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed fast list response with adapted ``values`` access.
        """
        return BitrixAPIValuesListFastResponse.from_dict(json_response, result_adapter=self._result_adapter)

    def _call(self) -> JSONDict:
        """
        Execute the request using fast ID-window pagination.

        Returns:
            Raw JSON response returned by ``call_list_fast``.
        """
        return self._bitrix_token.call_list_fast(
            api_method=self._api_method,
            params=self._params,
            descending=self._descending,
            limit=self._limit,
            **self._kwargs,
        )
