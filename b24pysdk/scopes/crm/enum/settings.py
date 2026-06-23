from ....api.requests import BitrixAPIValuesRequest
from ....schemas.crm.enum import CRMEnumItem, CRMEnumItemsData
from ....scopes.crm._base_crm import BaseCRM
from ....utils.functional import type_checker
from ....utils.types import Timeout

__all__ = [
    "Settings",
]


class Settings(BaseCRM):
    """"""

    @type_checker
    def mode(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[CRMEnumItemsData, CRMEnumItem]:
        """Get description of CRM operation modes.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/enum/crm-enum-settings-mode.html

        The method returns a list of CRM operation modes.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.mode,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=CRMEnumItem.from_bitrix_result,
        )
