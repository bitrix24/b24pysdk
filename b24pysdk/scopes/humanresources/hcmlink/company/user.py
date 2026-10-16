from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, JSONList, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for obtaining companies from an HR system to the current user.

    Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/index.html
    """

    @type_checker
    def list(
            self,
            *,
            limit: int = MISSING,
            offset: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Get current user HCM link company list

        Documentation: https://apidocs.bitrix24.com/api-reference/sign/hcm-link/humanresources-hcmlink-company-user-list.html

        The method retrieves companies from an HR system linked to the current Bitrix24 user.

        Args:
            limit: Number of records per page;

            offset: Offset for page navigation;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )
