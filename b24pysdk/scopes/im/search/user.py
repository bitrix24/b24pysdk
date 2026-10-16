from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for retrieving users.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/im-search-user-list.html
    """

    @type_checker
    def list(
            self,
            find: Text,
            *,
            business: Optional[bool] = MISSING,
            offset: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Find user

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/im-search-user-list.html

        The method allows you to search for users by first name, last name, job title, and department.

        Args:
            find: Search phrase;

            business: Search only among business users;

            offset: Offset for the user selection;

            limit: Number of items in the selection;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            FIND=find,
        )

        if business is not MISSING:
            params["BUSINESS"] = bool_to_bitrix(business, is_required=True)

        if offset is not MISSING:
            params["OFFSET"] = offset

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
