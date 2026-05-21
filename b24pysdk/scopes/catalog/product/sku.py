from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Sku",
]


class Sku(BaseEntity):
    """Methods for working with parent products.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/sku/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add parent product

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/sku/catalog-product-sku-add.html

        This method adds a parent product to the trade catalog.

        Args:
            fields: Field values for adding the parent product;

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
        """Delete head product

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/sku/catalog-product-sku-delete.html

        This method deletes the head product.

        Args:
            bitrix_id: Identifier of the head product;

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
    def download(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Download main product files

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/sku/catalog-product-sku-download.html

        This method downloads main product files based on the provided parameters.

        Args:
            fields: Field values for downloading main product files;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.download,
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
        """Get the values of the parent product fields

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/sku/catalog-product-sku-get.html

        The method returns the values of the parent product fields by identifier.

        Args:
            bitrix_id: Identifier of the parent product;

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
    def get_fields_by_filter(
            self,
            filter: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get parent product fields

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/sku/catalog-product-sku-get-fields-by-filter.html

        The method returns the fields of the parent product based on the filter.

        Args:
            filter: Filter to retrieve all fields of the parent product;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "filter": filter,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields_by_filter,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            select: Iterable[Text],
            filter: JSONDict,
            *,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of the parents product

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/sku/catalog-product-sku-list.html

        The method returns a list of parent products based on the filter.

        Args:
            select: An array with a list of fields to be selected;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible values for field correspond to the fields of the product sku object;

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

        if select.__class__ is not list:
            select = list(select)

        params: JSONDict = {
            "select": select,
            "filter": filter,
        }

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
        """Add parent product

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/sku/catalog-product-sku-update.html

        This method adds a parent product to the trade catalog.

        Args:
            bitrix_id: Identifier of the parent product;

            fields: Field values for updating the main product;

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
