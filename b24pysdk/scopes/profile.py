from ..bitrix_api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import Timeout
from ._base_scope import BaseScope

__all__ = [
    "Profile",
]


class Profile(BaseScope):
    """"""

    @type_checker
    def __call__(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self,
            timeout=timeout,
        )
