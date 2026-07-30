from typing import List, Optional, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Colleagues",
]


class Colleagues(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            *,
            user_data: Optional[Union[bool, B24BoolStrict]] = MISSING,
            offset: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Union[int, JSONDict]]]:
        """"""

        params: JSONDict = {}

        if user_data is not MISSING:
            params["USER_DATA"] = B24BoolStrict(user_data).to_b24()

        if offset is not MISSING:
            params["OFFSET"] = offset

        if limit is not MISSING:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )
