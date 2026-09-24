from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Propertyvariant",
]


class Propertyvariant(BaseEntity):
    """Methods for working with order property options of ENUM type in online store.

    Doumentation: https://apidocs.bitrix24.com/api-reference/sale/property-variant/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add property variant

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-variant/sale-property-variant-add.html

        The method adds a variant value for a property. It is applicable only for properties of type ENUM.

        Args:
            fields: Field values for creating a property variant;

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
        """Delete property variant

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-variant/sale-property-variant-delete.html

        The method deletes a property variant value of an order. It is applicable only for properties of type ENUM.

        Args:
            bitrix_id: Identifier of the property variant;

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
        """Get property variant value by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-variant/sale-property-variant-get.html

        The method retrieves the variant value of an order property. It is applicable only for properties of type ENUM.

        Args:
            bitrix_id: Identifier of the property variant;

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
        """Get available fields of property variant

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-variant/sale-property-variant-get-fields.html

        The method retrieves the available fields of property value variants.

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
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of property variants

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-variant/sale-property-variant-list.html

        The method retrieves a list of property value variants. This method is applicable only for properties of type ENUM.

        Args:
            select: An array of fields to be selected;

            filter: An object for filtering the selected records;

            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

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
        """Update property variant fields

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-variant/sale-property-variant-update.html

        The method updates the value variant of a property. It is applicable only for properties of type ENUM.

        Args:
            bitrix_id: Identifier of the property value variant;

            fields: Field values to update the property value variant;

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
