from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .base_crm import BaseCRM


class Category(BaseCRM):
    """The methods provide capabilities for managing CRM funnels.
    They allow you to retrieve fields, add, update, delete, and get lists of funnels.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/category/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            entity_type_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get funnel fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/category/crm-category-fields.html

        This method retrieves information about the fields of the sales funnels (directions) of the CRM entity.

        Args:
            entity_type_id: Identifier of the system or user-defined type of CRM entities for which to retrieve information about the fields of the funnel;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.fields,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            entity_type_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new funnel.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/category/crm-category-add.html

        This method creates a new funnel (direction) for the CRM object type with the identifier entity_type_id.

        Args:
            fields: Object format:

                {
                    name: "value",

                    sort: "value",

                    isDefault: "value",
                };

            entity_type_id: Identifier of the system or user-defined type of the CRM entity for which a new funnel will be created;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_method=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            entity_type_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get funnel by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/category/crm-category-get.html

        This method retrieves information about the funnel (direction) with the identifier id.

        Args:
            bitrix_id: Identifier of the funnel;

            entity_type_id: Identifier of the system or user-defined type of the CRM object for which we want to get the funnel;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            entity_type_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of funnels.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/category/crm-category-list.html

        This method retrieves a list of sales funnels (directions) that belong to the CRM object type with the identifier entityTypeId.

        Args:
            entity_type_id: Identifier of the system or user-defined type of CRM entities for which the list of funnels is to be retrieved;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            entity_type_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update funnel.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/category/crm-category-update.html

        This method updates the sales funnel (direction) with the identifier id, assigning it new field values from fields. If any field is missing in fields, its value will remain unchanged.

        Args:
            bitrix_id: Identifier of the funnel;

            fields: Object format:

                {
                    name: "value",

                    sort: "value",

                    isDefault: "value",
                };

            entity_type_id: Identifier of the system or user-defined type of CRM entities for which the funnel will be updated;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_method=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            entity_type_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete funnel.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/category/crm-category-delete.html

        This method deletes a sales funnel (direction) with the identifier id.

        Args:
            bitrix_id: Identifier of the funnel to be deleted;

            entity_type_id: Identifier of the system or user-defined type of the CRM entity from which the funnel will be deleted:

            timeout: Timeout in seconds.


        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
