from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "History",
]


class History(BaseEntity):
    """"""

    @type_checker
    def search(  # noqa: C901, PLR0912
            self,
            *,
            search_text: Optional[Text] = None,
            search_type: Optional[Text] = None,
            search_types: Optional[Iterable[Text]] = None,
            search_date: Optional[Text] = None,
            search_date_from: Optional[Text] = None,
            search_date_to: Optional[Text] = None,
            search_authors: Optional[Iterable[int]] = None,
            last_id: Optional[int] = None,
            limit: Optional[int] = None,
            convert_text: Optional[Text] = None,
            group_tag: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = dict()

        if search_text is not None:
            params["SEARCH_TEXT"] = search_text

        if search_type is not None:
            params["SEARCH_TYPE"] = search_type

        if search_types is not None:
            if search_types.__class__ is not list:
                search_types = list(search_types)
            params["SEARCH_TYPES"] = search_types

        if search_date is not None:
            params["SEARCH_DATE"] = search_date

        if search_date_from is not None:
            params["SEARCH_DATE_FROM"] = search_date_from

        if search_date_to is not None:
            params["SEARCH_DATE_TO"] = search_date_to

        if search_authors is not None:
            if search_authors.__class__ is not list:
                search_authors = list(search_authors)
            params["SEARCH_AUTHORS"] = search_authors

        if last_id is not None:
            params["LAST_ID"] = last_id

        if limit is not None:
            params["LIMIT"] = limit

        if convert_text is not None:
            params["CONVERT_TEXT"] = convert_text

        if group_tag is not None:
            params["GROUP_TAG"] = group_tag

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params or None,
            timeout=timeout,
        )
