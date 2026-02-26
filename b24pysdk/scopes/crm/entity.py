from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_crm import BaseCRM

__all__ = [
    "Entity",
]


class Entity(BaseCRM):
    """Method lets you to merge duplicates in CRM.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/index.html
    """

    @type_checker
    def merge_batch(
            self,
            *,
            params: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Merge duplicates

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/crm-entity-merge-batch.html

        The method merges multiple entities into one.

        Args:
            params: Object containing the entities to merge, which contains:

                - entityTypeId: Identifier of the CRM object type,

                - entityIds: array of identifiers of the entities to be merged;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.merge_batch,
            params=params,
            timeout=timeout,
        )
