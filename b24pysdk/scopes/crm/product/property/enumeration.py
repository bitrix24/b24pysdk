from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ..._base_crm import BaseCRM

__all__ = [
    "Enumeration",
]


class Enumeration(BaseCRM):
    """"""

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._fields(timeout=timeout)
