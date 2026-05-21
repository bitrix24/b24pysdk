from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Vat",
]


class Vat(BaseEntity):
    """Handle VAT rates in trade catalog.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/vat/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add VAT rate

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/vat/catalog-vat-add.html

        This method adds a new VAT rate.

        Args:
            fields: Field values for creating a new VAT rate;

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete VAT rate

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/vat/catalog-vat-delete.html

        This method deletes a VAT rate.

        Args:
            bitrix_id: Identifier of the VAT rate;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get VAT rate field values

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/vat/catalog-vat-get.html

        This method retrieves information about the VAT rate by its identifier.

        Args:
            bitrix_id: Identifier of the VAT rate;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get VAT rate fields

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/vat/catalog-vat-get-fields.html

        The method returns the fields of the VAT rate.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of VAT rates

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/vat/catalog-vat-list.html

        The method returns a list of VAT rates based on the filter.

        Args:
            select: An array with a list of fields to be selected;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible values for field correspond to the fields of the catalog VAT object;

            order: Object format:
                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the field name to sort by;

                - value_n is 'asc' for ascending or 'desc' for descending;

            start: Starting position for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = dict()

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        if start is not None:
            params["start"] = start

        if limit is not None:
            params["limit"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
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
        """Update VAT rate

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/vat/catalog-vat-update.html

        This method updates the VAT rate.

        Args:
            bitrix_id: Identifier of the VAT rate;

            fields: Field values for updating the VAT rate;

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
