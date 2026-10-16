from typing import Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for retrieving comments for a news feed post.

    Documentation: https://apidocs.bitrix24.com/api-reference/log/blogcomment/index.html
    """

    @type_checker
    def get(
            self,
            *,
            user_id: Optional[int] = MISSING,
            first_id: Optional[int] = MISSING,
            last_id: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get user comments

        Documentation: https://apidocs.bitrix24.com/api-reference/log/blogcomment/log-blogcomment-user-get.html

        The method returns a list of comments on a news feed post for the specified user and information about attached files.

        Args:
            user_id: The identifier of the user whose comments need to be retrieved;

            first_id: The method will return comments with identifiers greater than the specified value;

            last_id: The method will return comments with identifiers less than the specified value;

            limit: The number of records in the response;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if first_id is not MISSING:
            params["FIRST_ID"] = first_id

        if last_id is not MISSING:
            params["LAST_ID"] = last_id

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
