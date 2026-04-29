from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ProductPropertyFeature",
]


class ProductPropertyFeature(BaseEntity):
    """Handle operations related to Bitrix24 catalog product property and variation parameters.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-feature/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "productPropertyFeature"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add product property or variation parameter

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-feature/catalog-product-property-feature-add.html

        The method adds a parameter to a product or variation property.

        Args:
            fields: Set of fields for the new property parameter;

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
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get product property feature parameter or variations

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-feature/catalog-product-property-feature-get.html

        The method returns the product property feature parameter or variation by its identifier.

        Args:
            bitrix_id: Identifier of the property parameter;

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
    def get_available_features_by_property(
            self,
            property_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get available product property features or variations

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-feature/catalog-product-property-feature-get-available-features-by-property.html

        The method returns a list of available parameters for the specified product property or variation.

        Args:
            property_id: Identifier of the product property or variation;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "propertyId": property_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_available_features_by_property,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields of product property features or variations

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-feature/catalog-product-property-feature-get-fields.html

        The method returns a description of the fields for product property features or variations.

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
        """Get a list of product property feature parameters or variations

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-feature/catalog-product-property-feature-list.html

        The method returns a list of product property feature parameters and variations based on the filter.

        Args:
            select: An array containing the list of fields to select;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible keys correspond to the fields of the object;

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
        """Update product property or variation parameter

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product-property-feature/catalog-product-property-feature-update.html

        The method updates the parameter of a product or variation property.

        Args:
            bitrix_id: Identifier of the property parameter;

            fields: Set of fields for the updated property parameter;

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
