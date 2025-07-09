from typing import TYPE_CHECKING, Optional

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .timeline import Timeline


class Logmessage(BaseCRM):
    """"""

    def __init__(self, timeline: "Timeline"):
        super().__init__(timeline._scope)
        self._path = self._get_path(timeline)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._add(fields, timeout=timeout)

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
    def list(
            self,
            entity_type_id: int,
            entity_id: id,
            *,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        if order is not None:
            params["order"] = order

        if start is not None:
            params["start"] = start

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._list),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._delete(bitrix_id)
