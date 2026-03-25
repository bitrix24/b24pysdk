from typing import Iterable, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "List",
]


class List(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            bitrix_id: Iterable[Union[int, Text]],
            avatar_hr: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if bitrix_id.__class__ is not list:
            bitrix_id = list(bitrix_id)

        params = {
            "ID": bitrix_id,
        }

        if avatar_hr is not None:
            params["AVATAR_HR"] = B24BoolStrict(avatar_hr).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
