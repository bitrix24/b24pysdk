from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Scope",
]


class Scope(BaseEntity):
    """Class for helping to determine the scope.

    Documentation: https://apidocs.bitrix24.com/api-reference/index.html
    """

    @type_checker
    def list(
            self,
            *,
            filter_controller: Optional[Text] = MISSING,
            filter_method: Optional[Text] = MISSING,
            filter_module: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the method-to-scope mapping for all module

        Documentation: https://apidocs.bitrix24.com/api-reference/rest-v3.html

        The method helps to determine the scope when the method page does not specify it.

        Args:
            filter_controller: Filter by controller name;

            filter_method: Filter by method name;

            filter_module: Filter by module name;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter_controller is not MISSING:
            params["filterController"] = filter_controller

        if filter_method is not MISSING:
            params["filterMethod"] = filter_method

        if filter_module is not MISSING:
            params["filterModule"] = filter_module

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
