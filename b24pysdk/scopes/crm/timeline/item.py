from typing import Optional

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Item",
]


class Item(BaseCRM):
    """"""

    @type_checker
    def pin(
            self,
            bitrix_id: int,
            owner_type_id: int,
            owner_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Optional[bool]]:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.pin,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpin(
            self,
            bitrix_id: int,
            owner_type_id: int,
            owner_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Optional[bool]]:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "ownerTypeId": owner_type_id,
            "ownerId": owner_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unpin,
            params=params,
            timeout=timeout,
        )
