
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Booking",
]


class Booking(BaseEntity):
    """Handle operations related to Bitrix24 calendar resource bookings.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/resource/calendar-resource-booking-list.html
    """

    @type_checker
    def list(
            self,
            filter: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve bookings for calendar resources based on the provided filter criteria.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/resource/calendar-resource-booking-list.html

        This method fetches a list of bookings for calendar resources by applying the specified filter criteria. It allows querying bookings with specific conditions.

        Args:
            filter: Object format:
                {
                    "KEY": "value"
                }, where each key specifies a booking attribute to filter by, and its value defines the condition;

            timeout: Timeout in seconds for the API request;

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "filter": filter,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
