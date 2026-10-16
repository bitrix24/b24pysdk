from typing import List, Text

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Scope",
]


class Scope(BaseScope):
    """Class for retrieving available scopes to the current application.

    Documentation: https://apidocs.bitrix24.com/api-reference/common/index.html
    """

    @type_checker
    def __call__(
            self,
            full: bool = MISSING,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """Get a list of available permissions scope

        Documentation: https://apidocs.bitrix24.com/api-reference/common/system/scope.html

        The method returns a list of permissions.

        Args:
            full: If the parameter is set to true, the method will return the complete list of permissions;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if full is not MISSING:
            params["full"] = full

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )
