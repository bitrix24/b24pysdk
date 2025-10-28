from typing import Text

from ..bitrix_api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import Timeout
from ._base_scope import BaseScope

__all__ = [
    "Feature",
]


class Feature(BaseScope):
    """"""

    @type_checker
    def get(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
