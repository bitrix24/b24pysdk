from typing import Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Userfield",
]


class Userfield(BaseEntity):
    """A set of methods for managing custom fields in tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-field/index.html
    """

    @type_checker
    def add(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add custom field

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-field/task-item-user-field-add.html

        The method creates a custom field for a task.

        Args:
            params: Set of parameters for the created field;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "PARAMS": params,
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
        """Delete user field

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-field/task-item-user-field-delete.html

        The method removes a custom field from a task.

        Args:
            bitrix_id: Identifier of the custom field;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
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
        """Get custom task field by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-field/task-item-user-field-get.html

        The method retrieves the description of a custom task field by its ID.

        Args:
            bitrix_id: Identifier of the custom field;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getfields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get user field fields

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-field/task-item-user-field-get-fields.html

        The method retrieves a list of fields for task custom fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.getfields,
            timeout=timeout,
        )

    @type_checker
    def getlist(
            self,
            *,
            order: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of custom fields

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-field/task-item-user-field-get-list.html

        The method retrieves a list of custom fields for tasks.

        Args:
            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

            filter: Object for filtering the result;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["FILTER"] = filter

        if order is not MISSING:
            params["ORDER"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def gettypes(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of available data types

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-field/task-item-user-field-get-types.html

        The method retrieves the available types of custom fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.gettypes,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update user field

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-field/task-item-user-field-update.html

        The method updates the parameters of a task's user field.

        Args:
            bitrix_id: Identifier of the user field;

            data: Set of parameters to be updated for the field;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
            "DATA": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
