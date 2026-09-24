from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Settings",
]


class Settings(BaseEntity):
    """Class for retrieving settings of the time tracking tool.

    Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/index.html
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get report settings

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/timeman-timecontrol-reports-settings-get.html

        The method retrieves report settings for building the report interface of the time control tool.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
