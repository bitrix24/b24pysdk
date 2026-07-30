from typing import Optional

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "List",
]


class List(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            params: Optional[JSONDict] = MISSING,
            options: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        payload = dict()

        if params is not MISSING:
            payload["PARAMS"] = params

        if options is not MISSING:
            payload["OPTIONS"] = options

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=payload or None,
            timeout=timeout,
        )
