from functools import cached_property
from typing import Optional

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .client import Client
from .external_data import ExternalData

__all__ = [
    "Booking",
]


class Booking(BaseEntity):
    """Class for managing bookings.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/index.html
    """

    @cached_property
    def client(self) -> Client:
        """"""
        return Client(self)

    @cached_property
    def external_data(self) -> ExternalData:
        """"""
        return ExternalData(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add booking

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/booking-v1-booking-add.html

        The method adds a new booking for a resource.

        Args:
            fields: An object containing field values for creating a booking;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def createfromwaitlist(
            self,
            wait_list_id: int,
            *,
            fields: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a booking from the waitlist

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/booking-v1-booking-createfromwaitlist.html

        The method creates a booking based on an entry from the waitlist.

        Args:
             wait_list_id: Identifier of the entry in the waitlist;

             fields: Object containing field values for creating a booking;

             timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "waitListId": wait_list_id,
        }

        if fields is not MISSING:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.createfromwaitlist,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete booking

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/booking-v1-booking-delete.html

        The method removes a booking.

        Args:
            bitrix_id: Booking identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about booking

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/booking-v1-booking-get.html

        The method returns information about a booking by its identifier.

        Args:
            bitrix_id: Booking identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of bookings

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/booking-v1-booking-list.html

        The method returns a list of booking based on the filter.

        Args:
            filter: Object for filtering the list of bookings;

            order: Object for sorting the list of bookings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update booking

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/booking-v1-booking-update.html

        The method updates the booking information.

        Args:
            bitrix_id: Booking identifier;

            fields: Object containing field values for updating the booking;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
