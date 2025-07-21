from typing import TYPE_CHECKING

from ....bitrix_api.classes import BitrixAPIRequest
from ....scopes.crm.base_crm import BaseCRM
from ....utils.functional import type_checker
from ....utils.types import Timeout

if TYPE_CHECKING:
    from .enum import Enum


class Settings(BaseCRM):

    def __init__(self, enum: "Enum"):
        super().__init__(enum._scope)
        self._path = self._get_path(enum)

    @type_checker
    def mode(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.mode),
            timeout=timeout,
        )
