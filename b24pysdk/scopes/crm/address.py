from typing import Iterable, Optional, Text

from ..._bitrix_api_request import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict
from .base_crm import BaseCRM


class Address(BaseCRM):
    """The methods provide capabilities for managing addresses.
    They allow you to retrieve fields, add, update, delete, and get lists of addresses.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/addresses/index.html
    """

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get address fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/addresses/crm-address-fields.html

        The method returns a formal description of the address fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Add address.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/addresses/crm-address-add.html

        This method adds a new address for a property or lead. For the user, this address appears as the address of a contact, company, or lead.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields, timeout=timeout)

    @type_checker
    def update(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update address.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/addresses/crm-address-update.html

        This method updates the address for a contact or lead.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

                where values for the fields TYPE_ID, ENTITY_TYPE_ID, ENTITY_ID must be specified;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.update),
            params=params,
            timeout=timeout,
        )

    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get a list of addresses.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/addresses/crm-address-list.html

        The method returns a list of addresses based on the filter.

        Args:
            select: An array containing the list of fields to be selected;

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

                - field_n is the name of the field by which the selection will be sorted,

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            start: This parameter is used for pagination control;

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
    def delete(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Delete address.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/addresses/crm-address-delete.html

        This method deletes an address.

        Args:
            fields: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }

                where values for the fields TYPE_ID, ENTITY_TYPE_ID, ENTITY_ID must be specified;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.delete),
            params=params,
            timeout=timeout,
        )
