from typing import Optional, TYPE_CHECKING

from ...._bitrix_api_request import BitrixAPIRequest

from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .userfield import Userfield


class Enumeration(BaseCRM):
    """"""

    def __init__(self, userfield: "Userfield"):
        super().__init__(scope=userfield._scope)
        self._path = self._get_path(userfield)

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return super().fields(timeout=timeout)
