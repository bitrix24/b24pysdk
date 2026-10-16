from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Chat",
]


class Chat(BaseEntity):
    """Class for retrieving chats by names.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/index.html
    """

    @type_checker
    def list(
            self,
            *,
            find: Optional[Text] = MISSING,
            find_lines: Optional[Text] = MISSING,
            offset: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Find chats

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/search/im-search-chat-list.html

        The method performs a search for chats that the current user has access to.

        Args:
            find: Search phrase for querying indexed chat data;

            find_lines: Search phrase for finding chats among Open Channels;

            offset: Offset for the chat sample;

            limit: Number of items in the sample;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict()

        if find is not MISSING:
            params["FIND"] = find

        if find_lines is not MISSING:
            params["FIND_LINES"] = find_lines

        if offset is not MISSING:
            params["OFFSET"] = offset

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
