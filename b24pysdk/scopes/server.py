from datetime import datetime
from typing import Text

from ..api.requests import BitrixAPIValueRequest
from ..utils.converters import datetime_from_bitrix
from ..utils.functional import type_checker
from ..utils.types import Timeout
from ._base_scope import BaseScope

__all__ = [
    "Server",
]


class Server(BaseScope):
    """"""

    @type_checker
    def time(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[Text, datetime]:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.time,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=lambda result: datetime_from_bitrix(result, is_required=True),
        )
