from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Shipmentitem",
]


class Shipmentitem(BaseEntity):
    """Methods for working with shipment table section in the online store.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-item/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add an item to the shipment table part

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-item/sale-shipment-item-add.html

        The method adds an item to the shipment table part.

        Args:
            fields: Field values for creating an item in the shipment table part;

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
        """Delete shipment item from collection

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-item/sale-shipment-item-delete.html

        The method removes an item from the shipment's table part.

        Args:
            bitrix_id: Identifier of the shipment table item;

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
        """Accessing fields of the element

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-item/sale-shipment-item-get.html

        The method is designed to retrieve the values of all fields of the shipment item table element.

        Args:
            bitrix_id: Identifier of the shipment item table element;

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
        """Get fields of shipment item

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-item/sale-shipment-item-get-fields.html

        The method retrieves a list of available fields for shipment item table entries.

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
        """Get a list of shipment item table elements

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-item/sale-shipment-item-list.html

        The method retrieves a list of shipment item table elements.

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
        """Update an item in the shipment table part

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-item/sale-shipment-item-update.html

        The method updates an item in the shipment table part collection.

        Args:
            bitrix_id: Identifier of the shipment table part item;

            fields: Field values for updating the shipment table part item;

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
