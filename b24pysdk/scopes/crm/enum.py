from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .base_crm import BaseCRM


class Enum(BaseCRM):
    """"""

    @type_checker
    def getorderownertypes(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.getorderownertypes),
            timeout=timeout,
        )

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._fields(timeout=timeout)

    @type_checker
    def ownertype(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.ownertype),
            timeout=timeout,
        )
