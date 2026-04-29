from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Enum",
]


class Enum(BaseEntity):
    """Handle enumeration-related operations for the Bitrix24 Catalog scope.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/enum/index.html
    """

    @type_checker
    def get_round_types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve the list of catalog rounding types.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/enum/catalog-enum-get-round-types.html

        Returns enumeration values representing rounding types available in the catalog.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get_round_types,
            timeout=timeout,
        )

    @type_checker
    def get_store_document_types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Retrieve the list of store document types.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/enum/catalog-enum-get-store-document-types.html

        Returns enumeration values for store document types available via REST.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get_store_document_types,
            timeout=timeout,
        )
