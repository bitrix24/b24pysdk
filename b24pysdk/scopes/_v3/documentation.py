from ...api.requests import BitrixAPIRawRequest
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
    ) -> BitrixAPIRawRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIRawRequest,
        )
