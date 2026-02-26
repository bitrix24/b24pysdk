from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Counters",
]


class Counters(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            user_id: Optional[int] = None,
            group_id: Optional[int] = None,
            type: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if user_id is not None:
            params["userId"] = user_id

        if group_id is not None:
            params["groupId"] = group_id

        if type is not None:
            params["type"] = type

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
