from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Entity",
]


class Entity(BaseCRM):
    """"""

    @type_checker
    def items(
            self,
            entity_id: str,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the directory item by its symbolic identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-entity-items.html

        The method returns directory items by its symbolic identifier, sorted by the 'SORT' field.

        Args:
            entity_id: Symbolic identifier of the directory;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityId": entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.items,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get CRM status entity types.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-entity-types.html

        The method returns a description of the entity types.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.types,
            timeout=timeout,
        )
