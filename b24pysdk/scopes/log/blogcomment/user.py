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
    """"""

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
        """"""

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
