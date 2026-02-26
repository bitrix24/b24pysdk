from typing import Optional, Text

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
            scope: Optional[Text] = None,
            full: Optional[bool] = None,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if scope is not None:
            params["SCOPE"] = scope

        if full is not None:
            params["FULL"] = full

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )
