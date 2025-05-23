from typing import Iterable, Optional, TYPE_CHECKING, Union

from ..._bitrix_api_request import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict

from .base_crm import BaseCRM

if TYPE_CHECKING:
    from . import Lead, Deal, Quote


class Productrows(BaseCRM):
    """"""

    def __init__(self, item: Union["Lead", "Deal", "Quote"]):
        super().__init__(item._scope)
        self._path = self._get_path(item)

    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def set(
            self,
            bitrix_id: int,
            rows: Iterable[JSONDict],
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "rows": list(rows),
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.set),
            params=params,
            timeout=timeout,
        )
