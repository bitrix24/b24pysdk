from typing import Optional

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Idle",
]


class Idle(BaseEntity):
    """"""

    @type_checker
    def end(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.end,
            timeout=timeout,
        )

    @type_checker
    def start(
            self,
            *,
            ago: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params: JSONDict = {}

        if ago is not MISSING:
            params["AGO"] = ago

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params or None,
            timeout=timeout,
        )
