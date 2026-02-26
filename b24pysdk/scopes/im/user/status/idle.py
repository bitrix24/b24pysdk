from typing import Optional

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
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
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.end,
            timeout=timeout,
        )

    @type_checker
    def start(
            self,
            *,
            ago: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if ago is not None:
            params["AGO"] = ago

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params or None,
            timeout=timeout,
        )
