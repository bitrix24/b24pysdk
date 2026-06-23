from typing import Text

from ..api.requests import BitrixAPIValueRequest
from ..schemas.method import MethodGet, MethodGetData
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Method",
]


class Method(BaseScope):
    """"""

    @type_checker
    def get(
            self,
            name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[MethodGetData, MethodGet]:
        """"""

        params: JSONDict = {
            "name": name,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=MethodGet.from_bitrix,
        )
