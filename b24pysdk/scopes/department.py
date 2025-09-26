from typing import Optional, Text

from ..bitrix_api.classes import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import Timeout
from .scope import Scope

__all__ = [
    "Department",
]


class Department(Scope):
    """Class for managing departments.

    Documentation: https://apidocs.bitrix24.com/api-reference/departments/index.html
    """

    @type_checker
    def fields(
            self,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
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
            api_method=self.fields,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            name: Text,
            parent: int,
            sort: Optional[int] = None,
            uf_head: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
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

        params = {
            "NAME": name,
            "PARENT": parent,
        }

        if sort is not None:
            params["SORT"] = sort

        if uf_head is not None:
            params["UF_HEAD"] = uf_head

        return self._make_bitrix_api_request(
            api_method=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            sort: Optional[Text] = None,
            order: Optional[Text] = None,
            bitrix_id: Optional[int] = None,
            name: Optional[Text] = None,
            parent: Optional[int] = None,
            uf_head: Optional[int] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
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

        params = dict()

        if sort is not None:
            params["sort"] = sort

        if order is not None:
            params["order"] = order

        if bitrix_id is not None:
            params["ID"] = bitrix_id

        if name is not None:
            params["NAME"] = name

        if parent is not None:
            params["PARENT"] = parent

        if uf_head is not None:
            params["UF_HEAD"] = uf_head

        if start is not None:
            params["START"] = start

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            name: Optional[Text] = None,
            sort: Optional[int] = None,
            parent: Optional[int] = None,
            uf_head: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
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

        params = {
            "ID": bitrix_id,
        }

        if name is not None:
            params["NAME"] = name

        if sort is not None:
            params["SORT"] = sort

        if parent is not None:
            params["PARENT"] = parent

        if uf_head is not None:
            params["UF_HEAD"] = uf_head

        return self._make_bitrix_api_request(
            api_method=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
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

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
