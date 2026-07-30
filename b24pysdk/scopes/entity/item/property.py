from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Property",
]


class Property(BaseEntity):
    """Methods manage additional data within application elements

    Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/properties/index.html
    """

    @type_checker
    def get(
            self,
            entity: Text,
            *,
            property: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get properties of storage elements

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/properties/entity-item-property-get.html

        The method returns the properties of the application's data storage elements.

        Args:
            entity: Identifier of the application's data storage;

            property: Property code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ENTITY": entity,
        }

        if property is not MISSING:
            params["PROPERTY"] = property

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            entity: Text,
            property: Text,
            name: Text,
            type: Text,
            *,
            sort: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add property to data storage elements

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/properties/entity-item-property-add.html

        The method adds a property to the elements of the application's data storage.

        Args:
            entity: Identifier of the application's data storage;

            property: Property code;

            name: Name of property;

            type: Type of property;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "ENTITY": entity,
            "PROPERTY": property,
            "NAME": name,
            "TYPE": type,
        }

        if sort is not MISSING:
            params["SORT"] = sort

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            entity: Text,
            property: Text,
            *,
            property_new: Optional[Text] = MISSING,
            name: Optional[Text] = MISSING,
            type: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update property of storage elements

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/properties/entity-item-property-update.html

        The method modifies the property of elements in the application's data storage.

        Args:
            entity: Identifier of the application's data storage;

            property: Property code;

            property_new: New property code;

            name: Name of property;

            type: Type of property;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ENTITY": entity,
            "PROPERTY": property,
        }

        if property_new is not MISSING:
            params["PROPERTY_NEW"] = property_new

        if name is not MISSING:
            params["NAME"] = name

        if type is not MISSING:
            params["TYPE"] = type

        if sort is not MISSING:
            params["SORT"] = sort

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            entity: Text,
            property: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete property of storage elements

        Documentation: https://apidocs.bitrix24.com/api-reference/entity/items/properties/entity-item-property-delete.html

        The method removes a property from the application's data storage elements.

        Args:
            entity: Identifier of the application's data storage;

            property: Property code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ENTITY": entity,
            "PROPERTY": property,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

