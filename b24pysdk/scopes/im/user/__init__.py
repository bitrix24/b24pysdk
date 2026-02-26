from functools import cached_property
from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
from ..._base_entity import BaseEntity
from .list import List
from .status import Status

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            bitrix_id: Optional[Union[int, Text]] = None,
            avatar_hr: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if bitrix_id is not None:
            params["ID"] = bitrix_id

        if avatar_hr is not None:
            params["AVATAR_HR"] = B24BoolStrict(avatar_hr).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )

    @cached_property
    def list(self) -> List:
        """"""
        return List(self)

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)
