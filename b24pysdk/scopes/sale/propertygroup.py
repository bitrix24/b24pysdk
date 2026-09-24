from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Propertygroup",
]


class Propertygroup(BaseEntity):
    """Mehtods for working in property groups in the online store.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-group/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create property group

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-group/sale-property-group-add.html

        The method creates a property group.

        Args:
            fields: Field values for creating a property group;

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
        """Delete property

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-group/sale-property-group-delete.html

        The method deletes a property group.

        Args:
            bitrix_id: Identifier of the property group;

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
        """Get values of all fields in a property group by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-group/sale-property-group-get.html

        The method retrieves the values of all fields in a property group.

        Args:
            bitrix_id: Identifier of the property group;

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
        """Get available fields of property groups

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-group/sale-property-group-get-fields.html

        The method retrieves the available fields of property groups.

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
        """Get a list of property groups

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-group/sale-property-group-list.html

        The method retrieves a list of property groups.

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
        """Update property group fields

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/property-group/sale-property-group-update.html

        The method updates the fields of a property group.

        Args:
            bitrix_id: Identifier of the property group;

            fields: An array of fields to be updated;

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
