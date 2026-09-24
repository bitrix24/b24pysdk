from functools import cached_property
from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .offer import Offer
from .service import Service
from .sku import Sku

__all__ = [
    "Product",
]


class Product(BaseEntity):
    """Class for managing products in the trade catalog.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/index.html
    """

    @cached_property
    def offer(self) -> Offer:
        """"""
        return Offer(self)

    @cached_property
    def service(self) -> Service:
        """"""
        return Service(self)

    @cached_property
    def sku(self) -> Sku:
        """"""
        return Sku(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add product

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/catalog-product-add.html

        The method adds a product to the trading catalog.

        Args:
            fields: Field values for adding a new product as a structure;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
        """Delete product

        Documentatoin: https://apidocs.bitrix24.com/api-reference/catalog/product/catalog-product-delete.html

        The method removes a product from the trade catalog.

        Args:
            bitrix_id: Product identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
        """Download product files

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/catalog-product-download.html

        The method downloads product files from the trade catalog based on the provided parameters.

        Args:
            fields: Field values for downloading product files;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
        """Get product by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/catalog-product-get.html

        The method retrieves information about a product in the trade catalog by its ID.

        Args:
            bitrix_id: Identifier of the product;

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
    def get_fields_by_filter(
            self,
            filter: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get product fields by filter

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/catalog-product-get-fields-by-filter.html

        The method retrieves product fields based on a filter.

        Args:
            filter: Filter to retrieve all product fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of products by filter

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/catalog-product-list.html

        The method retrieves a list of products from the trade catalog based on filter.

        Args:
            select: An array containing a list of fields that need to be selected;

            filter: An object for filtering selected products;

            order: Object for sorting selected products;

            start: The parameter is used to control pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if select.__class__ is not list:
            select = list(select)

        params: JSONDict = {
            "select": select,
            "filter": filter,
        }

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
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
        """Update product

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/catalog-product-update.html

        The method updates a product in the trade catalog.

        Args:
            bitrix_id: Product identifier;

            fields: Field values for updating the product;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
