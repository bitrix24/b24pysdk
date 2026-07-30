from typing import Dict, Optional, Text

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
from ..objects.department import Department as DepartmentObject
from ..utils.functional import type_checker
from ..utils.types import JSONDict, JSONList, Timeout
from ._adapters import BitrixObjectAdapter, BitrixObjectsAdapter
from ._base_scope import BaseScope

__all__ = [
    "Department",
]


class Department(BaseScope):
    """Class for managing departments.

    Documentation: https://apidocs.bitrix24.com/api-reference/departments/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Dict[Text, Text]]:
        """
        Get fields of a department.

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/department-fields.html

        This method returns a list and description of available department fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            name: Text,
            parent: int,
            *,
            sort: Optional[int] = MISSING,
            uf_head: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[int, DepartmentObject]:
        """
        Add a new department.

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/department-add.html

        This method adds a new department to the company's structure.

        Args:
            name: Name of the department;

            parent: Parent department ID;

            sort: Department sorting field;

            uf_head: Identifier of the user who will become the head of the department;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "NAME": name,
            "PARENT": parent,
        }

        if sort is not MISSING:
            params["SORT"] = sort

        if uf_head is not MISSING:
            params["UF_HEAD"] = uf_head

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter(DepartmentObject, client=self._client),
        )

    @type_checker
    def get(
            self,
            *,
            sort: Optional[Text] = MISSING,
            order: Optional[Text] = MISSING,
            bitrix_id: Optional[int] = MISSING,
            name: Optional[Text] = MISSING,
            parent: Optional[int] = MISSING,
            uf_head: Optional[int] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, DepartmentObject]:
        """
        Get a list of departments with filtering.

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/department-get.html

        This method retrieves a list of departments, optionally filtered by provided parameters.

        Args:
            sort: Sort order for departments;

            order: Order logic for sorting;

            bitrix_id: Specific department ID to retrieve;

            name: Name of the department to retrieve;

            parent: Filter by parent department ID;

            uf_head: Filter by department head;

            start: Starting index for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if sort is not MISSING:
            params["sort"] = sort

        if order is not MISSING:
            params["order"] = order

        if bitrix_id is not MISSING:
            params["ID"] = bitrix_id

        if name is not MISSING:
            params["NAME"] = name

        if parent is not MISSING:
            params["PARENT"] = parent

        if uf_head is not MISSING:
            params["UF_HEAD"] = uf_head

        if start is not MISSING:
            params["START"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter(DepartmentObject, client=self._client),
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            *,
            name: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            parent: Optional[int] = MISSING,
            uf_head: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """
        Update an existing department.

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/department-update.html

        This method updates details of a specific department.

        Args:
            bitrix_id: ID of the department to update;

            name: New name for the department;

            sort: Sorting field of the department;

            parent: New parent department ID;

            uf_head: Identifier of the user who will be the head of the department;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": bitrix_id,
        }

        if name is not MISSING:
            params["NAME"] = name

        if sort is not MISSING:
            params["SORT"] = sort

        if parent is not MISSING:
            params["PARENT"] = parent

        if uf_head is not MISSING:
            params["UF_HEAD"] = uf_head

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
    ) -> BitrixAPIRequest[bool]:
        """
        Delete a department.

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/department-delete.html

        This method deletes a department based on the provided ID.

        Args:
            bitrix_id: ID of the department to delete;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
