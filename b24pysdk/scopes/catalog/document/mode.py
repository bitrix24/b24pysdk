from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Mode",
]


class Mode(BaseEntity):
    """Class for checking an availability of inventory accounting.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/index.html
    """

    @type_checker
    def status(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check the status of inventory management

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-mode-status.html

        The method checks the activity of inventory management.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.status,
            timeout=timeout,
        )
