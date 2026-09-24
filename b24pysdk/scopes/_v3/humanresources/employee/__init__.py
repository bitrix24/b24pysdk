from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .field import Field

__all__ = [
    "Employee",
]


class Employee(BaseEntity):
    """Class for retrieving employee's digital profiles.

    Documentation: https://apidocs.bitrix24.com/api-reference/departments/employee/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def count(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the number of employees

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/employee/humanresources-employee-count.html

        The method returns the number of unique employees in the company structure.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.count,
            timeout=timeout,
        )

    @type_checker
    def multidepartment(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get employees in multiple departments

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/employee/humanresources-employee-multidepartment.html

        The method returns employees who belong to multiple departments.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.multidepartment,
            timeout=timeout,
        )

    @type_checker
    def search(
            self,
            name: Text,
            *,
            node_id: Optional[int] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Find employees

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/employee/humanresources-employee-search.html

        The method searches for employees by name.

        Args:
            name: Search string for the employee's name;

            node_id: Identifier of the department or team to limit the search;

            select: List of employee fields to return;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "name": name,
        }

        if node_id is not MISSING:
            params["nodeId"] = node_id

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def subordinates(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get subordinates of employee

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/employee/humanresources-employee-subordinates.html

        The method returns the number of subordinates of the user by departments.

        Args:
            bitrix_id: Identifier of the user for whom to get subordinates;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.subordinates,
            params=params,
            timeout=timeout,
        )
