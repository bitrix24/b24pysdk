from typing import Optional

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker

from ..base_crm import BaseCRM

from .enumeration import Enumeration
from .settings import Settings


class Userfield(BaseCRM):

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._fields(timeout=timeout)

    @type_checker
    def types(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.types),
            timeout=timeout,
        )

    @property
    def enumeration(self) -> Enumeration:
        """"""
        return Enumeration(self)

    @property
    def settings(self) -> Settings:
        """"""
        return Settings(self)
