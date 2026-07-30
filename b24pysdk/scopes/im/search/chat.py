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
    """"""

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
        """"""

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
