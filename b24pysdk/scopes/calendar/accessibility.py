from typing import Iterable, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Accessibility",
]


class Accessibility(BaseEntity):
    """
    Handle operations related to Bitrix24 calendar user accessibility.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/
    """

    @type_checker
    def get(
            self,
            users: Iterable[int],
            from_date: Text,
            to: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the accessibility of specified users within a date range.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-event/calendar-accessibility-get.html

        This method retrieves the availability of users from the list.

        Args:
            users: List of user IDs whose availability is being checked;
            from_date: The start date in format 'YYYY-MM-DD';
            to: The end date in format 'YYYY-MM-DD';
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if users.__class__ is not list:
            users = list(users)

        params = {
            "users": users,
            "from": from_date,
            "to": to,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

