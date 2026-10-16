from datetime import datetime
from typing import Text

from ..api.requests import BitrixAPIValueRequest
from ..utils.converters import datetime_from_bitrix
from ..utils.functional import type_checker
from ..utils.types import Timeout
from ._adapters import BitrixResultAdapter
from ._base_scope import BaseScope

__all__ = [
    "Server",
]


class Server(BaseScope):
    """Class for obtaining current server time.

    Documentation: https://apidocs.bitrix24.com/api-reference/common/index.html
    """

    @type_checker
    def time(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[Text, datetime]:
        """Get current server time

        Documentation: https://apidocs.bitrix24.com/api-reference/common/system/server-time.html

        The method returns the current server time in the format YYYY-MM-DDThh:mm:ss±hh:mm.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.time,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixResultAdapter(lambda result: datetime_from_bitrix(result, is_required=True)),
        )
