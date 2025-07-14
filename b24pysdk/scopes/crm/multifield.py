from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .base_crm import BaseCRM


class Multifield(BaseCRM):
    """"""

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._fields(timeout=timeout)
