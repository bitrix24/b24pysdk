from typing import Optional

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Users",
]


class Users(BaseEntity):
    """Class for retrieving users in the specified department.

    Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/index.html
    """

    @type_checker
    def get(
            self,
            *,
            department_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of users

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/timecontrol/timeman-timecontrol-reports-users-get.html

        The method retrieves the list of users in the department.

        Args:
            department_id: The identifier of the department;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if department_id is not MISSING:
            params["DEPARTMENT_ID"] = department_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
