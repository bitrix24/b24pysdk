from typing import Optional

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_crm import BaseCRM

__all__ = [
    "Type",
]


class Type(BaseCRM):
    """The methods provide capabilities for working with SPAs.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-object-types/index.html#methods-for-working-with-spas
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get custom fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-object-types/crm-type-fields.html

        This method retrieves information about the custom fields of the smart process settings.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new custom type (SPA).

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-object-types/crm-type-add.html

        This method creates a new SPA.

        Args:
            fields: Field values for adding a new SPA;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get custom type by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-object-types/crm-type-get.html

        This method retrieves information about the SPA with the identifier ID.

        Args:
            bitrix_id: Identifier of the SPA;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def get_by_entity_type_id(
            self,
            entity_type_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get smart process type by entityTypeId.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-object-types/crm-type-get-by-entity-type-id.html

        This method retrieves information about the SPA with the smart process type identifier entityTypeId.

        Args:
            entity_type_id: Identifier of the smart process type;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_by_entity_type_id,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of custom types.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-object-types/crm-type-list.html

        This method retrieves a list of smart process settings.

        Args:
            filter: Object format:
                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n
                };

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

            start: This parameter is used for pagination control;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._list(
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update user type.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-object-types/crm-type-update.html

        This method updates an existing SPA by its identifier ID.

        Args:
            bitrix_id: Identifier of the SPA;

            fields: Field values for adding a new SPA;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id,
            fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete custom type.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/user-defined-object-types/crm-type-delete.html

        This method deletes an existing SPA by its ID. You can only delete an SPA if there are no associated CRM entities.

        Args:
            bitrix_id: Identifier of the SPA;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)
