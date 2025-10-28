from typing import Iterable, Optional, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Recurring",
]


class Recurring(BaseCRM):
    """Methods provide capabilities for managing recurring deals.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/deals/recurring-deals/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of fields for the recurring deal template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/deals/recurring-deals/crm-deal-recurring-fields.html

        The method returns a list of fields for configuring the recurring deal template with descriptions.

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
        """Create a new recurring deal

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/deals/recurring-deals/crm-deal-recurring-add.html

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }, where each key-value pair represents a field of the deal and its corresponding value;

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
        """Get the fields of the recurring deal template settings by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/deals/recurring-deals/crm-deal-recurring-get.html

        The method returns the fields of the recurring deal template settings by identifier.

        Args:
            bitrix_id: Identifier of the recurring deal template settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get a list of recurring deal template settings

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/deals/recurring-deals/crm-deal-recurring-list.html

        The method returns a list of recurring deal template settings based on the filter.

        Args:
            select: List of fields that should be populated in the selected elements;

            filter: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);
            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            select=select,
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
        """Update existing settings for the recurring deal template

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/deals/recurring-deals/crm-deal-recurring-update.html

        The method updates the existing settings for the recurring deal template.

        Args:
            bitrix_id: Identifier of the recurring deal template settings;

            fields: Object format:

                {
                    field_to update: value_1,

                    ...,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(bitrix_id, fields, timeout=timeout)

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete existing configuration for recurring deal template

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/deals/recurring-deals/crm-deal-recurring-delete.html

        The method removes the existing configuration for the recurring deal template.

        Args:
            bitrix_id: Identifier of the recurring deal template configuration;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)

    @type_checker
    def expose(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new deal from the template

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/deals/recurring-deals/crm-deal-recurring-expose.html

        The method creates a new deal from the template.

        Args:
            bitrix_id: Identifier of the recurring deal template settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.expose,
            params=params,
            timeout=timeout,
        )
