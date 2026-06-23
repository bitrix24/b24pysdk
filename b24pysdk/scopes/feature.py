from typing import Text

from ..api.requests import BitrixAPIValueRequest
from ..schemas.feature import FeatureGet, FeatureGetData
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
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
    ) -> BitrixAPIValueRequest[FeatureGetData, FeatureGet]:
        """"""

        params: JSONDict = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=FeatureGet.from_bitrix,
        )
