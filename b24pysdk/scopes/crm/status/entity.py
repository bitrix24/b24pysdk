from typing import Text

from ....api.requests import BitrixAPIValuesRequest
from ....schemas.crm.status_entity import CRMStatusEntityItem, CRMStatusEntityItemsData, CRMStatusEntityType, CRMStatusEntityTypesData
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Entity",
]


class Entity(BaseCRM):
    """"""

    @type_checker
    def items(
            self,
            entity_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[CRMStatusEntityItemsData, CRMStatusEntityItem]:
        """Get the directory item by its symbolic identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-entity-items.html

        The method returns directory items by its symbolic identifier, sorted by the 'SORT' field.

        Args:
            entity_id: Symbolic identifier of the directory;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """

        params: JSONDict = {
            "entityId": entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.items,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=CRMStatusEntityItem.from_bitrix_result,
        )

    @type_checker
    def types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[CRMStatusEntityTypesData, CRMStatusEntityType]:
        """Get CRM status entity types.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/status/crm-status-entity-types.html

        The method returns a description of the entity types.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIValuesRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.types,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=CRMStatusEntityType.from_bitrix_result,
        )
