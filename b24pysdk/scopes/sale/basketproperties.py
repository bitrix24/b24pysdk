from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Basketproperties",
]


class Basketproperties(BaseEntity):
    """Methods for working with basket properties.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-properties/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a property for a basket item

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-properties/sale-basket-properties-add.html

        The method adds a property for an item (position) in the basket of an order.

        Args:
            fields: Field values for creating a property of a basket item (position);

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
        """Delete basket property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-properties/sale-basket-properties-delete.html

        The method removes a property for an item (position) in the basket of an order.

        Args:
            bitrix_id: Identifier of the basket item (position) property;

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
        """Get the value of the basket property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-properties/sale-basket-properties-get.html

        The method retrieves the property for an item (position) in the basket of an order by its identifier.

        Args:
            bitrix_id: Identifier of the basket item (position) property;

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
        """Get fields of basket properties

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-properties/sale-basket-properties-get-fields.html

        The method retrieves a list of property fields. Each field is described as a settings structure.

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
    def list(
        self,
        *,
        select: Optional[Iterable[Text]] = MISSING,
        filter: Optional[JSONDict] = MISSING,
        order: Optional[JSONDict] = MISSING,
        start: Optional[int] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of basket properties

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-properties/sale-basket-properties-list.html

        The method retrieves a set of properties for the items (positions) in the basket, selected based on a filter.

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
        """Change the property of the basket item

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/basket-properties/sale-basket-properties-update.html

        The method modifies the property for an item (position) in the basket of an order.

        Args:
            bitrix_id: Identifier of the order item;

            fields: An array of fields to be modified;

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
