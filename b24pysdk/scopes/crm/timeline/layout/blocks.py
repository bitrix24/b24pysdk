from typing import Optional

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ..._base_crm import BaseCRM

__all__ = [
    "Blocks",
]


class Blocks(BaseCRM):
    """"""

    @type_checker
    def get(
            self,
            entity_type_id: int,
            entity_id: int,
            timeline_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params: JSONDict = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "timelineId": timeline_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            entity_type_id: int,
            entity_id: int,
            timeline_id: int,
            layout: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params: JSONDict = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "timelineId": timeline_id,
            "layout": layout,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            entity_type_id: int,
            entity_id: int,
            timeline_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Optional[bool]]:
        """"""

        params: JSONDict = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "timelineId": timeline_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

