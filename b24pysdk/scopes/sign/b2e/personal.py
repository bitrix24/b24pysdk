from typing import Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Personal",
]


class Personal(BaseEntity):
    """"""

    @type_checker
    def tail(
            self,
            *,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if limit is not None:
            params["limit"] = limit

        if offset is not None:
            params["offset"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.tail,
            params=params or None,
            timeout=timeout,
        )
