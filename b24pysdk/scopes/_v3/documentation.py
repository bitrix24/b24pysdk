from ...api.requests import BitrixAPIRawRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_scope import BaseScope

__all__ = [
    "Documentation",
]


class Documentation(BaseScope):
    """Class for retrieving OpenAPI documentation.

    Documentation: https://apidocs.bitrix24.com/api-reference/rest-v3.html
    """

    @type_checker
    def __call__(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRawRequest:
        """Obtain documentation

        Documentation: https://apidocs.bitrix24.com/api-reference/rest-v3.html

        The method returns JSON in OpenAPI format with the list of available methods and object schemas.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIRawRequest,
        )
