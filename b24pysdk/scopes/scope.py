from typing import List, Optional, Text

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Scope",
]


class Scope(BaseScope):
    """"""

    @type_checker
    def __call__(
            self,
            full: Optional[bool] = MISSING,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[Text]]:
        """"""

        params: JSONDict = {}

        if full is not MISSING:
            params["full"] = full

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )
