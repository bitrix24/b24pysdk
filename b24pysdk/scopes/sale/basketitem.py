from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Basketitem",
]


class Basketitem(BaseEntity):
    """Methods for managing shopping carts in online store.

    Documantetion: https://apidocs.bitrix24.com/api-reference/sale/basket-item/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add item

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-add.html

        The method adds an item to the cart of an existing order.

        Args:
            fields: Field values for creating an item (position) in the cart of the order;

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
    def add_catalog_product(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a product to the cart of an existing order

        Documentatoin: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-add-catalog-product.html

        The method adds a position (item) with a product or service from the catalog module to the cart of an existing order.

        Args:
            fields: Field values for creating an item (position) in the order cart;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add_catalog_product,
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
        """Remove item

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-delete.html

        The method removes an item (position) from the cart in the order.

        Args:
            bitrix_id: Identifier of the cart item;

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
    def get(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about a basket item

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-get.html

        The method retrieves information about a basket item (position).

        Args:
            bitrix_id: Identifier of the basket item;

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
        """Get available fields of the basket item

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-get-fields.html

        The method returns a list of available fields of the basket item.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def get_fields_catalog_product(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get available fields of a basket item

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-get-catalog-product-fields.html

        The method retrieves a list of available fields for a basket item for adding and updating basket items.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields_catalog_product,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        select: Optional[Iterable[Text]] = MISSING,
        filter: Optional[JSONDict] = MISSING,
        order: Optional[JSONDict] = MISSING,
        start: Optional[int] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of items

        Documentatoin: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-list.html

        The method retrieves a set of items (positions) in the cart filtered by the specified criteria.

        Args:
            select: An array of fields to be selected;

            filter: An object for filtering the selected records;

            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if filter is not MISSING:
            params["filter"] = filter

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
        """Change the position of the basket in an existing order

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-update.html

        The method modifies the position of the basket in an existing order.

        Args:
            bitrix_id: Identifier of the order item;

            fields: Values of the fields to be modified;

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

    @type_checker
    def update_catalog_product(
        self,
        bitrix_id: int,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Change the basket item position of an existing order

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-item/sale-basket-item-update-catalog-product.html

        The method changes the basket item position (catalog product) of an existing order.

        Args:
            bitrix_id: Identifier of the basket item;

            fields: Object with modifiable fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update_catalog_product,
            params=params,
            timeout=timeout,
        )
