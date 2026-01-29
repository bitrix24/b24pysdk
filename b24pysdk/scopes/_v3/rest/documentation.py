from ....bitrix_api.requests import BitrixBaseAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Documentation",
]


class Documentation(BaseEntity):
    """"""

    @type_checker
    def openapi(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixBaseAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.openapi,
            timeout=timeout,
            bitrix_api_request_type=BitrixBaseAPIRequest,
        )
