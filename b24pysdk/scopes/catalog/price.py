from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Price",
]


class Price(BaseEntity):
    """Handle operations related to Bitrix24 catalog prices.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a product price.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price/catalog-price-add.html

        The method adds a new price for a product.

        Args:
            fields: Object format:
                {
                    "catalogGroupId": integer,

                    "currency": string,

                    "price": number,

                    "productId": integer,

                    "quantityFrom": integer,

                    "quantityTo": integer,

                    "extraId": integer
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

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
        """Delete a product price by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price/catalog-price-delete.html

        The method removes the product price.

        Args:
            bitrix_id: Identifier of the price resource;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

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
        """Retrieve fields of a product price by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price/catalog-price-get.html

        The method returns information about the product price by its ID.

        Args:
            bitrix_id: Identifier of the price resource;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

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
        """Fetch the list of available fields for the price resource.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price/catalog-price-get-fields.html

        The method returns the fields of a product's price.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""
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
        """Get a list of prices by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price/catalog-price-list.html

        The method returns a list of product prices based on the filter.

        Args:
            select: List of fields corresponding to available fields;

            filter: Object format:
                {
                    field_1: value_1,

                    ...,
                };

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_1 is the name of the field by which the selection will be sorted;

                - value_1 is a string value equal to 'ASC' (ascending sort) or 'DESC' (descending sort);

            start: Page number for HTTPS pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

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
    def modify(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Modify the collection of prices for a product.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price/catalog-price-modify.html

        The method updates the product price collection.

        Args:
            fields: Object format:
                {
                    "product": {

                        "id": integer,

                        "prices": [
                            ...
                        ]
                    }
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.modify,
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
        """Update fields of a product price.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price/catalog-price-update.html

        Args:
            bitrix_id: Identifier of the price resource;

            fields: Object format:
                {
                    "catalogGroupId": integer,

                    "currency": string,

                    "price": number,

                    "productId": integer,

                    "quantityFrom": integer,

                    "quantityTo": integer,

                    "extraId": integer
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest."""

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
