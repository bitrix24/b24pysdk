from ..api.requests import BitrixAPIValueRequest
from ..schemas.profile import Profile as ProfileSchema
from ..schemas.profile import ProfileData
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
    ) -> BitrixAPIValueRequest[ProfileData, ProfileSchema]:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=ProfileSchema.from_bitrix,
        )
