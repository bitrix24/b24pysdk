from typing import Iterable, Text

from ..bitrix_api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import Timeout
from ._base_scope import BaseScope

__all__ = [
    "Access",
]


class Access(BaseScope):
    """"""

    @type_checker
    def name(
            self,
            access: Iterable[Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if access.__class__ is not list:
            access = list(access)

        params = {
            "ACCESS": access,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.name,
            params=params,
            timeout=timeout,
        )
