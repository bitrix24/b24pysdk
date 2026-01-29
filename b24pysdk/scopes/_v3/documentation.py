from ...bitrix_api.requests import BitrixBaseAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_scope import BaseScope

__all__ = [
    "Documentation",
]


class Documentation(BaseScope):
    """"""

    @type_checker
    def __call__(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixBaseAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self,
            timeout=timeout,
            bitrix_api_request_type=BitrixBaseAPIRequest,
        )
