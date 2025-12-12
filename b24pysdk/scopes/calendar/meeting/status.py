from typing import Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Status",
]


class Status(BaseEntity):
    """Handle operations related to Bitrix24 meeting status.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/
    """

    @type_checker
    def get(
            self,
            event_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the participation status of the current user in a calendar event.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-meeting-status-get.html

        This method retrieves the participation status of the current user in the event.

        Args:
            event_id: The ID of the event;

            timeout: Timeout in seconds.

        Returns:
            An instance of BitrixAPIRequest containing the user participation status.
        """

        params = {
            "eventId": event_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            event_id: int,
            status: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Set the participation status in an event for the current user.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-meeting-status-set.html

        This method sets the participation status in an event for the current user.

        Args:
            event_id: The ID of the event;

            status: The new participation status to set;

            timeout: Timeout in seconds.

        Returns:
            An instance of BitrixAPIRequest confirming the status update.
        """

        params = {
            "eventId": event_id,
            "status": status,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
