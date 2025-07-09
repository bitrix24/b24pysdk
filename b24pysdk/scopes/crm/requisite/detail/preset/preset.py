from ......bitrix_api.classes import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import Timeout
from ..detail import Detail
from .field import Field


class Preset(Detail):
    """"""

    @property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def countries(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.countries),
            timeout=timeout,
        )
