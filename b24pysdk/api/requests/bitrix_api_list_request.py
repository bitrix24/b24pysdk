from abc import ABC
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from ...utils.types import JSONDict
from ..responses import AbstractBitrixAPIListResponse, BitrixAPIListFastResponse, BitrixAPIListResponse
from .bitrix_api_base_request import BitrixAPIBaseRequest

if TYPE_CHECKING:
    from .bitrix_api_request import BitrixAPIRequest

__all__ = [
    "BitrixAPIListFastRequest",
    "BitrixAPIListRequest",
]

_BALRPT = TypeVar("_BALRPT", bound=AbstractBitrixAPIListResponse)


class _AbstractBitrixAPIListRequest(BitrixAPIBaseRequest[_BALRPT], ABC, Generic[_BALRPT]):
    """
    Base class for lazy Bitrix24 list request objects.

    Reuses an existing ``BitrixAPIRequest`` and executes it through list-style
    pagination helpers while preserving the original method, parameters, token,
    and requester options.
    """

    __slots__ = ("_limit",)

    _limit: Optional[int]

    def __init__(
            self,
            *,
            bitrix_api_request: "BitrixAPIRequest",
            limit: Optional[int] = None,
            **kwargs,
    ):
        """
        Initialize a list request from a base API request.

        Args:
            bitrix_api_request: Source API request to convert into a list request.
            limit: Optional maximum number of items to retrieve.
            **kwargs: Extra options overriding or extending source request options.
        """
        super().__init__(
            bitrix_token=bitrix_api_request._bitrix_token,
            api_method=bitrix_api_request._api_method,
            params=bitrix_api_request._params,
            **bitrix_api_request._kwargs | kwargs,
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


class BitrixAPIListRequest(_AbstractBitrixAPIListRequest[BitrixAPIListResponse]):
    """
    Lazy request object for loading a paginated Bitrix24 list.

    Executes the wrapped API method through ``call_list`` and converts the
    response into ``BitrixAPIListResponse``.
    """

    __slots__ = ()

    @staticmethod
    def _convert_response(json_response: JSONDict) -> BitrixAPIListResponse:
        """
        Convert raw JSON response into ``BitrixAPIListResponse``.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed Bitrix list response.
        """
        return BitrixAPIListResponse.from_dict(json_response)

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


class BitrixAPIListFastRequest(_AbstractBitrixAPIListRequest[BitrixAPIListFastResponse]):
    """
    Lazy request object for loading a Bitrix24 list with fast ID pagination.

    Executes the wrapped API method through ``call_list_fast`` and converts the
    response into ``BitrixAPIListFastResponse``. The resulting response contains
    a lazy one-time generator, so list items are fetched progressively during
    iteration.
    """

    __slots__ = ("_descending",)

    _descending: bool

    def __init__(
            self,
            *,
            bitrix_api_request: "BitrixAPIRequest",
            descending: bool = False,
            limit: Optional[int] = None,
            **kwargs,
    ):
        """
        Initialize a fast list request from a base API request.

        Args:
            bitrix_api_request: Source API request to convert into a fast list request.
            descending: Whether to retrieve items in descending ID order.
            limit: Optional maximum number of items to retrieve.
            **kwargs: Extra options overriding or extending source request options.
        """
        super().__init__(
            bitrix_api_request=bitrix_api_request,
            limit=limit,
            **bitrix_api_request._kwargs | kwargs,
        )
        self._descending = descending

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"api_method='{self._api_method}', "
            f"params={self._params}, "
            f"descending={self._descending}, "
            f"limit={self._limit})"
        )

    @staticmethod
    def _convert_response(json_response: JSONDict) -> BitrixAPIListFastResponse:
        """
        Convert raw JSON response into ``BitrixAPIListFastResponse``.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed fast list response with lazy result generator.
        """
        return BitrixAPIListFastResponse.from_dict(json_response)

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
