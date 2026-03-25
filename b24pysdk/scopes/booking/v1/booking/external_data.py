from typing import Iterable, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "ExternalData",
]


class ExternalData(BaseEntity):
    """Handle operations related to Bitrix24 booking external data links.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/external-data/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "externalData"

    @type_checker
    def list(
            self,
            booking_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve external data links for a specific booking.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/external-data/booking-v1-booking-externaldata-list.html

        This method fetches the external objects linked to the specified booking.

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
            external_data: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Set external data links for a specific booking.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/external-data/booking-v1-booking-externaldata-set.html

        This method assigns external objects to the specified booking.

        Args:
            booking_id: Identifier of the booking;

            external_data: Object format:
                [
                    {
                        "moduleId": value,
                        "entityTypeId": value,
                        "value": value,
                    },
                ];

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if external_data.__class__ is not list:
            external_data = list(external_data)

        params = {
            "bookingId": booking_id,
            "externalData": external_data,
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
        Remove all external data links from a specific booking.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking/external-data/booking-v1-booking-externaldata-unset.html

        This method detaches any external objects linked to the specified booking.

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
