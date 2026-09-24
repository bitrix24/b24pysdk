from typing import Literal

from ....api.requests import BitrixAPIValueRequest
from ....constants.crm import CRMSettingsMode
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Mode",
]


class Mode(BaseCRM):
    """Class for obtaining

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/index.html
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[Literal[1, 2], CRMSettingsMode]:
        """Determine the current CRM operating mode

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/crm-settings-mode-get.html

        The method returns the current settings of the CRM operating mode: with (classic) or without leads (simple).

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=CRMSettingsMode,
        )
