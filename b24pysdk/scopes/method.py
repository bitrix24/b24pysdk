from typing import Text

from ..api.requests import BitrixAPIValueRequest
from ..schemas.method import MethodGet, MethodGetData
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._adapters import BitrixSchemaAdapter
from ._base_scope import BaseScope

__all__ = [
    "Method",
]


class Method(BaseScope):
    """Class for checking existence of a method.

    Documentation: https://apidocs.bitrix24.com/api-reference/common/system/index.html
    """

    @type_checker
    def get(
            self,
            name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[MethodGetData, MethodGet]:
        """Get a list of available methods

        Documentation: https://apidocs.bitrix24.com/api-reference/common/system/method-get.html

        The method returns two parameters, which determines the existence of the method in Bitrix24 and its availability for invocation.

        Args:
            name: The name of the method to check in lowercase;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "name": name,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixSchemaAdapter(MethodGet),
        )
