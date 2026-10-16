from typing import List, Optional, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Colleagues",
]


class Colleagues(BaseEntity):
    """Class for retrieving information about colleagues.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/departments/index.html
    """

    @type_checker
    def list(
            self,
            *,
            user_data: Optional[bool] = MISSING,
            offset: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Union[int, JSONDict]]]:
        """Get the list of colleagues for the current user

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/departments/im-department-colleagues-list.html

        The method retrieves a list of colleagues for the current user.

        Args:
            user_data: Returned detailed user data;

            offset: Offset for user selection;

            limit: Number of items in the selection;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if user_data is not MISSING:
            params["USER_DATA"] = bool_to_bitrix(user_data, is_required=True)

        if offset is not MISSING:
            params["OFFSET"] = offset

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )
