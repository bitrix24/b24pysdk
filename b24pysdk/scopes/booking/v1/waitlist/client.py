from typing import Iterable

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Client",
]


class Client(BaseEntity):
    """Handle operations related to clients of a waitlist record in Bitrix24 Booking.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/client/index.html
    """

    @type_checker
    def set(
            self,
            wait_list_id: int,
            clients: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Set clients for a specific waitlist record.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/client/booking-v1-waitlist-client-set.html

        This method assigns the provided clients to the specified waitlist record.

        Args:
            wait_list_id: Identifier of the waitlist record (waitListId);

            clients: Array of objects containing information about clients;

            timeout: Request timeout;

        Returns:
            Instance of BitrixAPIRequest.
        """

        if clients.__class__ is not list:
            clients = list(clients)

        params: JSONDict = {
            "waitListId": wait_list_id,
            "clients": clients,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            wait_list_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the list of clients for a specific waitlist record.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/client/booking-v1-waitlist-client-list.html

        Args:
            wait_list_id: Identifier of the waitlist record (waitListId);

            timeout: Request timeout;

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "waitListId": wait_list_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unset(
            self,
            wait_list_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Remove clients from a specific waitlist record.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/client/booking-v1-waitlist-client-unset.html

        Args:
            wait_list_id: Identifier of the waitlist record (waitListId);

            timeout: Request timeout;

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "waitListId": wait_list_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unset,
            params=params,
            timeout=timeout,
        )
