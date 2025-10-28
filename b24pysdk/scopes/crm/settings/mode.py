from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Mode",
]


class Mode(BaseCRM):
    """"""

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
