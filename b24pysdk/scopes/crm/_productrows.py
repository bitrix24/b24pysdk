from typing import Iterable

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_crm import BaseCRM

__all__ = [
    "Productrows",
]


class Productrows(BaseCRM):
    """"""

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def set(
            self,
            bitrix_id: int,
            rows: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if rows.__class__ is not list:
            rows = list(rows)

        params = {
            "id": bitrix_id,
            "rows": rows,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
