from typing import Annotated, Iterable, Literal, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Shipmentproperty",
]


class Shipmentproperty(BaseEntity):
    """Class for working with shipping properties in the online store.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add shipment property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property/sale-shipment-property-add.html

        The method adds a shipment property.

        Args:
            fields: Field values for creating a shipment property;

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
        """Delete shipment property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property/sale-shipment-property-delete.html

        The method deletes a shipment property.

        Args:
            bitrix_id: Identifier of the shipment property;

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
        """Get shipment property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property/sale-shipment-property-get.html

        The method retrieves the shipment property.

        Args:
            bitrix_id: Identifier of the shipment property;

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
    def getfieldsbytype(
        self,
        type: Annotated[Text, Literal["STRING", "Y/N", "NUMBER", "ENUM", "FILE", "DATE", "LOCATION", "ADDRESS"]],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields and settings of shipment property for a specific property type

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property/sale-shipment-property-get-fields-by-type.html

        The method retrieves the available fields of shipment properties by property type.

        Args:
            type: Shipment property type;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "type": type,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getfieldsbytype,
            params=params,
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
        """Get a list of shipment properties

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property/sale-shipment-property-list.html

        The method retrieves a list of shipment properties.

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
        """Update shipment property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/shipment-property/sale-shipment-property-update.html

        The method updates the shipment property.

        Args:
            bitrix_id: Identifier of the shipment property;

            fields: Field values for updating the shipment property;

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
