from typing import Text

from ..api.requests import BitrixAPIValueRequest
from ..schemas.feature import FeatureGet, FeatureGetData
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._adapters import BitrixSchemaAdapter
from ._base_scope import BaseScope

__all__ = [
    "Feature",
]


class Feature(BaseScope):
    """Class for checking the availability of functionality in Bitrix24.

    Documentation: https://apidocs.bitrix24.com/api-reference/common/system/index.html
    """

    @type_checker
    def get(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[FeatureGetData, FeatureGet]:
        """Get information about feature availability in Bitrix24

        Documentation: https://apidocs.bitrix24.com/api-reference/common/system/feature-get.html

        The method returns information about the availability of features in a specific Bitrix24.

        Args:
            code: Key of the event;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixSchemaAdapter(FeatureGet),
        )
