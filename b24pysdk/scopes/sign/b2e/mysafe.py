from typing import Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Mysafe",
]


class Mysafe(BaseEntity):
    """"""

    @type_checker
    def tail(
            self,
            *,
            limit: Optional[int] = MISSING,
            offset: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.tail,
            params=params or None,
            timeout=timeout,
        )
