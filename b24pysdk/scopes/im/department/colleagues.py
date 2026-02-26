from typing import Optional, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
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
            user_data: Optional[Union[bool, B24BoolStrict]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if user_data is not None:
            params["USER_DATA"] = B24BoolStrict(user_data).to_b24()

        if offset is not None:
            params["OFFSET"] = offset

        if limit is not None:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )
