from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Field",
]


class Field(BaseEntity):
    """Class for retrieving employee fields.

    Documentation: https://apidocs.bitrix24.com/api-reference/departments/employee/index.html
    """

    @type_checker
    def get(
            self,
            name: Text,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of  employee fields

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/employee/humanresources-employee-field-get.html

        The method returns a list of available employee fields.

        Args:
            name: The name of the field whose description is to be retrieved;

            select: List of field descriptions to return in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "name": name,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of  employee fields

        Documentation: https://apidocs.bitrix24.com/api-reference/departments/employee/humanresources-employee-field-list.html

        The method returns a list of available employee fields.

        Args:
            select: List of field descriptions to return in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )
