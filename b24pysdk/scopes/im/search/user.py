from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
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
            business: Optional[Union[bool, B24BoolStrict]] = None,
            avatar_hr: Optional[Union[bool, B24BoolStrict]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            FIND=find,
        )

        if business is not None:
            params["BUSINESS"] = B24BoolStrict(business).to_b24()

        if avatar_hr is not None:
            params["AVATAR_HR"] = B24BoolStrict(avatar_hr).to_b24()

        if offset is not None:
            params["OFFSET"] = offset

        if limit is not None:
            params["LIMIT"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
