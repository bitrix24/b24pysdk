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
    """"""

    @type_checker
    def list(
            self,
            find: Text,
            *,
            business: Optional[bool] = MISSING,
            avatar_hr: Optional[bool] = MISSING,
            offset: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """"""

        params = dict(
            FIND=find,
        )

        if business is not MISSING:
            params["BUSINESS"] = bool_to_bitrix(business, is_required=True)

        if avatar_hr is not MISSING:
            params["AVATAR_HR"] = bool_to_bitrix(avatar_hr, is_required=True)

        if offset is not MISSING:
            params["OFFSET"] = offset

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
