from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Shipmentpropertyvalue",
]


class Shipmentpropertyvalue(BaseEntity):
    """Class for managing shipping property values in the online store

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property-value/index.html
    """

    @type_checker
    def delete(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete shipment property value

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property-value/sale-shipment-propertyvalue-delete.html

        The method deletes the shipment property value.

        Args:
            bitrix_id: The ID of the shipment property value;

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
        """Get shipment property value by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property-value/sale-shipment-property-value-get.html

        The method retrieves the values of the shipment property.

        Args:
            bitrix_id: The ID of the shipment property value;

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
        """Get available fields of shipment property values

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property-value/sale-shipment-property-value-get-fields.html

        The method retrieves the available fields of shipment property values.

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
        """Get a list of shipment property values

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property-value/sale-shipment-property-value-list.html

        The method retrieves a list of shipment property values.

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
    def modify(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update shipment property values

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property-value/sale-shipment-property-value-modify.html

        The method updates the shipment property values.

        Args:
            fields: The root element that carries the request parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.modify,
            params=params,
            timeout=timeout,
        )
