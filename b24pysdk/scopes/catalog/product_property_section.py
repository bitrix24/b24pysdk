from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ProductPropertySection",
]


class ProductPropertySection(BaseEntity):
    """Handle section settings for a product or variation property.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-section/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "productPropertySection"

    @type_checker
    def get(
            self,
            property_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get section settings of property

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-section/catalog-product-property-section-get.html

        The method returns the section settings of a product property or variation by the property ID.

        Args:
            property_id: The identifier of the product property or variation;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "propertyId": property_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
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
        """Get a list of section settings

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-section/catalog-product-property-section-list.html

        The method returns a list of section settings for product properties and variations based on a filter.

        Args:
            select: An array containing the list of fields to select;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible keys correspond to the fields available in the select parameter;

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
    def set(
            self,
            property_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set section settings for property

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-section/catalog-product-property-section-set.html

        The method sets the section settings for a product property or variation.

        Args:
            property_id: Identifier of the product property or variation;

            fields: Fields for the section settings of the property;

            timeout: Timeout in seconds.

         Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "propertyId": property_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
