
from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Settings",
]


class Settings(BaseEntity):
    """Handle operations related to Bitrix24 calendar user settings.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the user calendar settings.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-user-settings-get.html

        Fetches the Bitrix24 calendar user settings for the current user.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest containing the user's calendar settings.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            settings: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Set the user calendar settings.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-user-settings-set.html

        Updates the Bitrix24 calendar settings for the current user with the provided settings.

        Args:
            settings: Object format containing the user calendar settings. Includes keys such as view, meetSection, crmSection, etc.

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest indicating the success of the operation.
        """

        params = {
            "settings": settings,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
