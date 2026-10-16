from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Revision",
]


class Revision(BaseEntity):
    """Class for retrieving information about API revision.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about API revision

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/imopenlines-revision-get.html

        The method retrieves information about the API revisions of open channels.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
