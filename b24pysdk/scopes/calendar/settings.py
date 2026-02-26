from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Settings",
]


class Settings(BaseEntity):
    """
    Handle operations related to Bitrix24 calendar settings.

    Documentation: https://apidocs.bitrix24.com/api-reference/calendar/
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve calendar settings.

        Documentation: https://apidocs.bitrix24.com/api-reference/calendar/calendar-settings-get.html

        This method retrieves the main calendar settings. Only an administrator of the account can modify the main settings.

        Args:
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
