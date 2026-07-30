from typing import List, Optional, Text

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Events",
]


class Events(BaseScope):
    """"""

    @type_checker
    def __call__(
            self,
            scope: Optional[Text] = MISSING,
            full: Optional[bool] = MISSING,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """"""

        params: JSONDict = {}

        if scope is not MISSING:
            params["SCOPE"] = scope

        if full is not MISSING:
            params["FULL"] = full

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )
