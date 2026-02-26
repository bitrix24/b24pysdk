from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_crm import BaseCRM

__all__ = [
    "Vat",
]


class Vat(BaseCRM):
    """The methods provide capabilities for managing VAT rates in trade catalog.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/vat/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create VAT rate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/vat/crm-vat-add.html

        The method creates a new VAT rate in CRM.

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
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete VAT rate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/vat/crm-vat-delete.html

        The method removes a VAT rate by its identifier.

        Args:
            bitrix_id: Identifier of the VAT rate to be deleted;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get VAT rate by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/vat/crm-vat-get.html

        The method returns the VAT rate parameters by ID.

        Args:
            bitrix_id: Identifier of the VAT rate to be deleted;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get VAT rate fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/vat/crm-vat-fields.html

        The method returns the description of VAT rate fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of VAT rates by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/vat/crm-vat-list.html

        The method returns a list of VAT rates based on the filter.

        Args:
            order: Object format:
                {
                    field_1: value_1,
                    field_2: value_2,
                    ...,
                    field_n: value_n,
                },

                where

                    - field_n is the name of the field by which the selection will be sorted

                    - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);

            filter: Object format:
                {
                    field_1: value_1,
                    field_2: value_2,
                    ...,
                    field_n: value_n,
                };

            select: Array of returned fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            select=select,
            filter=filter,
            order=order,
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
        """Update existing VAT rate.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/auxiliary/vat/crm-vat-update.html

        The method updates the parameters of an existing VAT rate.

        Args:
            bitrix_id: Identifier of the VAT rate to be updated;

            fields: Array of fields to update;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id=bitrix_id,
            fields=fields,
            timeout=timeout,
        )
