from typing import TYPE_CHECKING

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .status import Status


class Entity(BaseCRM):
    """"""

    def __init__(self, status: "Status"):
        super().__init__(status._scope)
        self._path = self._get_path(status)

    @type_checker
    def items(
            self,
            entity_id: str,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityId": entity_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.items),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.types),
            timeout=timeout,
        )
