from typing import Optional

from ...utils.types import JSONDict
from ..responses import BitrixAPIResponse
from .bitrix_api_base_request import BitrixAPIBaseRequest
from .bitrix_api_list_request import BitrixAPIListFastRequest, BitrixAPIListRequest

__all__ = [
    "BitrixAPIRequest",
]


class BitrixAPIRequest(BitrixAPIBaseRequest[BitrixAPIResponse]):
    """
    Lazy request object for a standard Bitrix24 API method call.

    Converts the raw JSON response into ``BitrixAPIResponse`` and provides
    helpers for treating the same request as a paginated list request.
    """

    __slots__ = ()

    @staticmethod
    def _convert_response(json_response: JSONDict) -> BitrixAPIResponse:
        """
        Convert raw JSON response into ``BitrixAPIResponse``.

        Args:
            json_response: Raw JSON response returned by Bitrix24.

        Returns:
            Parsed Bitrix API response.
        """
        return BitrixAPIResponse.from_dict(json_response)

    def as_list(
            self,
            limit: Optional[int] = None,
    ) -> BitrixAPIListRequest:
        """
        Create a paginated list request from this API request.

        Args:
            limit: Optional maximum number of items to load.

        Returns:
            List request using the same API method, parameters, token, and
            requester options.
        """
        return BitrixAPIListRequest(
            bitrix_api_request=self,
            limit=limit,
            **self._kwargs,
        )

    def as_list_fast(
            self,
            descending: bool = False,
            limit: Optional[int] = None,
    ) -> BitrixAPIListFastRequest:
        """
        Create a fast paginated list request from this API request.

        Args:
            descending: Whether to retrieve items in descending ID order.
            limit: Optional maximum number of items to retrieve.

        Returns:
            Fast list request using ID-window pagination with the same API
            method, parameters, token, and requester options.
        """
        return BitrixAPIListFastRequest(
            bitrix_api_request=self,
            descending=descending,
            limit=limit,
            **self._kwargs,
        )
