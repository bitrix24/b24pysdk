from typing import TYPE_CHECKING, Iterable, Optional, Text

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .requisite import Requisite


class Link(BaseCRM):
    """"""

    def __init__(self, requisite: "Requisite"):
        super().__init__(requisite._scope)
        self._path = self._get_path(requisite)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._fields(timeout=timeout)

    @type_checker
    def get(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.get),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._list(
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "fields": fields,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.register),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.unregister),
            params=params,
            timeout=timeout,
        )
