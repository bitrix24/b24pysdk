from typing import Iterable, Text

from ..api.requests import BitrixAPIValueRequest
from ..schemas.access import AccessNamesData, AccessNamesDict
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
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
    ) -> BitrixAPIValueRequest[AccessNamesData, AccessNamesDict]:
        """"""

        if access.__class__ is not list:
            access = list(access)

        params: JSONDict = {
            "ACCESS": access,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.name,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=AccessNamesDict.from_bitrix,
        )
