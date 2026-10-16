from typing import Iterable, Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Employees",
]


class Employees(BaseEntity):
    """Class for retrieving list of employees from departments.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/departments/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: Iterable[int],
            *,
            user_data: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get a list of employees from departments

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/departments/im-department-employees-get.html

        The method retrieves a list of employees from the specified departments.

        Args:
            bitrix_id: An array of department IDs;

            user_data: Return detailed user data;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if bitrix_id.__class__ is not list:
            bitrix_id = list(bitrix_id)

        params = dict(
            ID=bitrix_id,
        )

        if user_data is not MISSING:
            params["USER_DATA"] = bool_to_bitrix(user_data, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
