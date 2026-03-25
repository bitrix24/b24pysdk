from typing import Iterable

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Client",
]


class Client(BaseEntity):
    """
    Handle operations related to Bitrix24 booking clients linked to a booking.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/client/index.html
    """

    @type_checker
    def list(
            self,
            booking_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the list of clients linked to a specific booking.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/client/booking-v1-booking-client-list.html

        This method returns the clients associated with the provided booking.

        Args:

            booking_id: Identifier of the booking;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "bookingId": booking_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            booking_id: int,
            clients: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Set clients for a specific booking.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/client/booking-v1-booking-client-set.html

        This method assigns clients to the specified booking.

        Args:
            booking_id: Identifier of the booking; can be obtained via booking.v1.booking.add and booking.v1.booking.list;

            clients: Object format:
                [
                    {
                        "id": integer,
                        "type": {
                            "module": "crm",
                            "code": "CONTACT" | "COMPANY",
                        },
                    }
                ];

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if clients.__class__ is not list:
            clients = list(clients)

        params = {
            "bookingId": booking_id,
            "clients": clients,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unset(
            self,
            booking_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Remove all clients from a specific booking.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/client/booking-v1-booking-client-unset.html

        his method detaches any clients linked to the specified booking.

        Args:
            booking_id: Identifier of the booking;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "bookingId": booking_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unset,
            params=params,
            timeout=timeout,
        )
