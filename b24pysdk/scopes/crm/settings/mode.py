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
    """"""

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[Literal[1, 2], CRMSettingsMode]:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=CRMSettingsMode,
        )
