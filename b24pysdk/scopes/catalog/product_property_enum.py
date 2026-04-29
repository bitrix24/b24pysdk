from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ProductPropertyEnum",
]


class ProductPropertyEnum(BaseEntity):
    """Handle operations related to Bitrix24 catalog product list properties.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-enum/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "productPropertyEnum"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add value to list property

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-enum/catalog-product-property-enum-add.html

        The method adds a value to a list property.

        Args:
            fields: Set of fields for the new list value;

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
        """Delete the value of the list property

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-enum/catalog-product-property-enum-delete.html

        The method removes the value of a list property.

        Args:
            bitrix_id: Identifier of the list property;

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
        """Get the value of the list property

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-enum/catalog-product-property-enum-get.html

        The method returns the value of a list property by its identifier.

        Args:
            bitrix_id: Identifier of the list property;

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
        """Get fields of list property values

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-enum/catalog-product-property-enum-get-fields.html

        The method returns the description of the fields for list property values.

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
        """Get a list of list property values

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-enum/catalog-product-property-enum-list.html

        The method returns a list of values for list properties based on the filter.

        Args:
            select: An array containing the list of fields to select;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible keys correspond to product list property fields;

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
        """Update the value of the list property

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-enum/catalog-product-property-enum-update.html

        The method updates the value of a list property.

        Args:
            bitrix_id: Identifier of the list property value;

            fields: Set of fields for the updated list value;

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
