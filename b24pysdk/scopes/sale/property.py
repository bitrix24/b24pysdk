from typing import Annotated, Iterable, Literal, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Property",
]


class Property(BaseEntity):
    """A set of methods for working with order properties on online store.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/property/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add order property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property/sale-property-add.html

        The method adds an order property.

        Args:
            fields: Field values for creating an order property;

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
        """Delete order property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property/sale-property-delete.html

        The method deletes an order property.

        Args:
            bitrix_id: Identifier of the order property;

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
        """Get order property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property/sale-property-get.html

        The method retrieves the order property.

        Args:
            bitrix_id: Identifier of the order property;

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
        """Get fields and settings for a specific type

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property/sale-property-get-fields-by-type.html

        The method retrieves the available fields of order properties by property type.

        Args:
            type: Order property type;

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
        """Get the list of order properties

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property/sale-property-list.html

        The method retrieves a list of order properties.

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
        """Update order property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property/sale-property-update.html

        The method updates the order property.

        Args:
            bitrix_id: Identifier of the order property;

            fields: Field values for creating the order property;

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
