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
    "Waitlist",
]


class Waitlist(BaseEntity):
    """Class for working with waitlists.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/index.html
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
        """Add waitlist

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/booking-v1-waitlist-add.html

        The method adds an entry to the waitlist.

        Args:
            fields: An object containing field values for creating an entry in the waitlist;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def createfrombooking(
            self,
            booking_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a waitlist entry from booking

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/booking-v1-waitlist-createfrombooking.html

        The method creates a waitlist entry based on an existing booking.

        Args:
            booking_id: Booking identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "bookingId": booking_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.createfrombooking,
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
        """Delete entry

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/booking-v1-waitlist-delete.html

        The method removes an entry from the waitlist.

        Args:
            bitrix_id: Booking identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
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
        """Get a record from the waitlist

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/booking-v1-waitlist-get.html

        The method returns information about a waitlist record by its identifier.

        Args:
             bitrix_id: Identifier of the waitlist record;

             timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
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
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of records from the waitlist

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/booking-v1-waitlist-list.html

        The method returns a list of records from the waitlist based on the filter.

        Args:
            filter: An object for filtering waitlist records;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

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
        """Update a record in the waitlist

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/waitlist/booking-v1-waitlist-update.html

        The method updates the information of a record in the waitlist.

        Args:
            bitrix_id: Identifier of the waitlist record;

            fields: An object containing field values for updating the record;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
