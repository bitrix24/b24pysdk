from ..api.requests import BitrixAPIValueRequest
from ..schemas.profile import Profile as ProfileSchema
from ..schemas.profile import ProfileData
from ..utils.functional import type_checker
from ..utils.types import Timeout
from ._adapters import BitrixSchemaAdapter
from ._base_scope import BaseScope

__all__ = [
    "Profile",
]


class Profile(BaseScope):
    """Class for retrieving information about the user.

    Documentation: https://apidocs.bitrix24.com/api-reference/common/users/index.html
    """

    @type_checker
    def __call__(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[ProfileData, ProfileSchema]:
        """Get basic information about the current user profile

        Documentation: https://apidocs.bitrix24.com/api-reference/common/users/profile.html

        The method returns basic information about the current user without any scopes.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixSchemaAdapter(ProfileSchema),
        )
