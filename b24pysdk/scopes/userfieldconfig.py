from typing import Optional, Text

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Userfieldconfig",
]


class Userfieldconfig(BaseScope):
    """Class for managing custom fields.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/userfieldconfig/index.html
    """

    @type_checker
    def add(
            self,
            module_id: Text,
            field: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add custom field

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/userfieldconfig/userfieldconfig-add.html

        The method adds a new custom field.

        Args:
            module_id: Module identifier where the field is created;

            field: Object with custom field settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "moduleId": module_id,
            "field": field,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            module_id: Text,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete user field

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/userfieldconfig/userfieldconfig-delete.html

        The method removes a user field.

        Args:
            module_id: Identifier of the module from which the field is being deleted;

            bitrix_id: Identifier of the user field settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "moduleId": module_id,
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
            module_id: Text,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get user field settings

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/userfieldconfig/userfieldconfig-get.html

        The method returns the settings of a user field by its identifier.

        Args:
            module_id: Identifier of the module from which the field is being deleted;

            bitrix_id: Identifier of the user field settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "moduleId": module_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_types(
            self,
            module_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get available user field types

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/userfieldconfig/userfieldconfig-get-types.html

        The method returns a set of available user field types for the module.

        Args:
            module_id: Identifier of the module for which to retrieve available field types;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "moduleId": module_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_types,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            module_id: Text,
            *,
            select: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of user field settings

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/userfieldconfig/userfieldconfig-list.html

        The method returns a list of user field settings based on the filter.

        Args:
            module_id: Identifier of the module from which the field is being deleted;

            select: Set of fields to return;

            order: Object for ordering;

            filter: Object for filtering;

            start: Offset for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "moduleId": module_id,
        }

        optional_params = {
            "select": select,
            "order": order,
            "filter": filter,
            "start": start,
        }

        if optional_params.get("select") is not MISSING:
            params["select"] = optional_params.get("select")

        if optional_params.get("order") is not MISSING:
            params["order"] = optional_params.get("order")

        if optional_params.get("filter") is not MISSING:
            params["filter"] = optional_params.get("filter")

        if optional_params.get("start") is not MISSING:
            params["start"] = optional_params.get("start")

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            module_id: Text,
            bitrix_id: int,
            *,
            field: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update user field

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/userfieldconfig/userfieldconfig-update.html

        The method updates the settings of an existing user field.

        Args:
            module_id: Identifier of the module from which the field is being updated;

            bitrix_id: Identifier of the user field settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "moduleId": module_id,
            "id": bitrix_id,
        }

        if field is not MISSING:
            params["field"] = field

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
