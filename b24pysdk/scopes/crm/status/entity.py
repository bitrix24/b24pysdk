from typing import TYPE_CHECKING

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .status import Status


class Entity(BaseCRM):
    """"""

    def __init__(self, status: "Status"):
        super().__init__(status._scope)
        self._path = self._get_path(status)

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

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.items),
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
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.types),
            timeout=timeout,
        )
