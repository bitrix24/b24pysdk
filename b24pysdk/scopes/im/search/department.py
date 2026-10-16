from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Department",
]


class Department(BaseEntity):
    """Class for retrieving departments by their name.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/index.html
    """

    @type_checker
    def list(
            self,
            find: Text,
            *,
            user_data: Optional[bool] = MISSING,
            offset: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Find departments

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/im-search-department-list.html

        The method performs a search for departments by their full name.

        Args:
            find: Search phrase for finding the beginning of words in the full name of the department;

            user_data: Return the manager's data in the field;

            offset: Offset for the department selection;

            limit: Number of items in the selection;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            FIND=find,
        )

        if user_data is not MISSING:
            params["USER_DATA"] = bool_to_bitrix(user_data, is_required=True)

        if offset is not MISSING:
            params["OFFSET"] = offset

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
