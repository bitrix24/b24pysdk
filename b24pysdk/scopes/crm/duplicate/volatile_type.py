from typing import Annotated, Literal, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM

__all__ = [
    "VolatileType",
]


class VolatileType(BaseCRM):
    """The methods provide capabilities to set up duplicate search.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/volatile-type/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            entity_type_id: Optional[Annotated[Text, Literal[1, 3, 4]]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of fields for duplicate search

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/volatile-type/crm-duplicate-volatile-type-fields.html

        The method returns a list of standard and custom fields that can be used for finding duplicates in leads, contacts and companies.

        Args:
            entity_type_id: Identifier of the object, where possible values are:

                - 1 - lead,

                - 3 - contact,

                - 4 - company;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict()

        if entity_type_id is not None:
            params["entityTypeId"] = entity_type_id

        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of custom fields involved in duplicate search

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/volatile-type/crm-duplicate-volatile-type-list.html

        The method returns a list of custom fields that are already used for duplicate searches in leads, contacts and companies.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            *,
            entity_type_id: Annotated[Text, Literal[1, 3, 4]],
            field_code: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a field to the duplicate search

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/volatile-type/crm-duplicate-volatile-type-register.html

        The method adds a field to the duplicate search functionality for leads, contacts or companies.

        Args:
            entity_type_id: Identifier of the object, where possible values are:

                - 1 - lead,

                - 3 - contact,

                - 4 - company;

            field_code: The code of the field to be added to the duplicate search;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "fieldCode": field_code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove field from duplicate search

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/duplicates/volatile-type/crm-duplicate-volatile-type-unregister.html

        The method removes a custom field from the duplicate search.

        Args:
            bitrix_id: Identifier of the field record to be removed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
