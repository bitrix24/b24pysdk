from typing import Optional

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Userfield",
]


class Userfield(BaseEntity):
    """Manage user-defined fields in the Bitrix24 system.

    Documentation: https://apidocs.bitrix24.com/api-reference/user/userfields/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Add a custom field.

        Documentation: https://apidocs.bitrix24.com/api-reference/user/userfields/user-userfield-add.html

        This method allows adding custom fields to the existing entities.

        Args:
            fields: A dictionary of field parameters to create;

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
    def list(
            self,
            *,
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve a list of custom fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/user/userfields/user-userfield-list.html

        This method retrieves a list of user fields with optional ordering and filtering.

        Args:
            order: A dictionary to sort the fields;

            filter: A dictionary to filter the fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if order is not None:
            params["order"] = order

        if filter is not None:
            params["filter"] = filter

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
        """
        Update a custom field.

        Documentation: https://apidocs.bitrix24.com/api-reference/user/userfields/user-userfield-update.html

        This method modifies the properties of the specified user field.

        Args:
            bitrix_id: The ID of the user field to update;

            fields: A dictionary of field parameters to update;

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
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Delete a custom field

        Documentation: https://apidocs.bitrix24.com/api-reference/user/userfields/user-userfield-delete.html

        This method removes a custom field from the system.

        Args:
            bitrix_id: The ID of the user field to delete;

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
