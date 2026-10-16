from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "History",
]


class History(BaseEntity):
    """Class for searching through notification history.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/index.html
    """

    @type_checker
    def search(  # noqa: C901, PLR0912
            self,
            *,
            search_text: Optional[Text] = MISSING,
            search_type: Optional[Text] = MISSING,
            search_types: Optional[Iterable[Text]] = MISSING,
            search_date: Optional[Text] = MISSING,
            search_date_from: Optional[Text] = MISSING,
            search_date_to: Optional[Text] = MISSING,
            search_authors: Optional[Iterable[int]] = MISSING,
            last_id: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            convert_text: Optional[Text] = MISSING,
            group_tag: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Searching notification history

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-history-search.html

        The method performs a search through the user's notification history.

        Args:
            search_text: Search text;

            search_type: Filter by notification type;

            search_types: Array of filters by notification types;

            search_date: Date filter in ISO 8601 format;

            search_date_from: Start of the date range in ISO 8601 format;

            search_date_to: End of the date range in ISO 8601 format;

            search_authors: Array of notification author identifiers for filtering;

            last_id: Identifier of the last notification from the previous page to load the next one;

            limit: Number of notifications per page;

            convert_text: Convert notification text;

            group_tag: Group tag for notifications for additional filtering;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if search_text is not MISSING:
            params["SEARCH_TEXT"] = search_text

        if search_type is not MISSING:
            params["SEARCH_TYPE"] = search_type

        if search_types is not MISSING:
            if search_types.__class__ is not list:
                search_types = list(search_types)
            params["SEARCH_TYPES"] = search_types

        if search_date is not MISSING:
            params["SEARCH_DATE"] = search_date

        if search_date_from is not MISSING:
            params["SEARCH_DATE_FROM"] = search_date_from

        if search_date_to is not MISSING:
            params["SEARCH_DATE_TO"] = search_date_to

        if search_authors is not MISSING:
            if search_authors.__class__ is not list:
                search_authors = list(search_authors)
            params["SEARCH_AUTHORS"] = search_authors

        if last_id is not MISSING:
            params["LAST_ID"] = last_id

        if limit is not MISSING:
            params["LIMIT"] = limit

        if convert_text is not MISSING:
            params["CONVERT_TEXT"] = convert_text

        if group_tag is not MISSING:
            params["GROUP_TAG"] = group_tag

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params or None,
            timeout=timeout,
        )
