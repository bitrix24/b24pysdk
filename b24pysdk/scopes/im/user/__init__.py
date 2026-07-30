from functools import cached_property
from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .list import List
from .status import Status

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @cached_property
    def list(self) -> List:
        """"""
        return List(self)

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)

    @type_checker
    def get(
            self,
            *,
            bitrix_id: Optional[Union[int, Text]] = MISSING,
            avatar_hr: Optional[Union[bool, B24BoolStrict]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params: JSONDict = {}

        if bitrix_id is not MISSING:
            params["ID"] = bitrix_id

        if avatar_hr is not MISSING:
            params["AVATAR_HR"] = B24BoolStrict(avatar_hr).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
