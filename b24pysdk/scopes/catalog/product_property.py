from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ProductProperty",
]


class ProductProperty(BaseEntity):
    """Handle operations related to Bitrix24 catalog product properties.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "productProperty"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add product property or variation.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property/catalog-product-property-add.html

        The method adds a property to a product or variation.

        Args:
            fields: Set of fields for the new property;

            timeout: Timeout in seconds.

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
        """Delete product property or variation

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property/catalog-product-property-delete.html

        The method removes a product property or variation.

        Args:
            bitrix_id: Identifier of the property;

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
        """Get product or variation property by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property/catalog-product-property-get.html

        The method returns the values of the product or variation property fields.

        Args:
            bitrix_id: Identifier of the property;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
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
        """Get product or variation property fields

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property/catalog-product-property-get-fields.html

        The method returns the fields of product or variation properties.

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
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of properties

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property/catalog-product-property-list.html

        The method returns a list of product properties and variations based on the filter.

        Args:
            select: An array containing the list of fields to select;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible keys correspond to product property fields;

            order: Object format:
                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the field name to sort by;

                - value_n is 'ASC' for ascending or 'DESC' for descending;

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
        """Update product or variation property

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property/catalog-product-property-update.html

        The method modifies the fields of a product or variation property.

        Args:
            bitrix_id: Property identifier;

            fields: Set of fields to update the property;

            timeout: Timeout in seconds.

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
