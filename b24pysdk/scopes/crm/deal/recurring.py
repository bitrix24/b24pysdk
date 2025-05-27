from typing import Iterable, Optional, Text

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict

from ..base_crm import BaseCRM
from .deal import Deal


class Recurring(BaseCRM):
    """"""

    def __init__(self, deal: Deal):
        super().__init__(deal._scope)
        self._path = self._get_path(deal)

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._fields(timeout=timeout)

    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._add(fields, timeout=timeout)

    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._get(bitrix_id, timeout=timeout)

    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._list(
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._update(bitrix_id, fields, timeout=timeout)

    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._delete(bitrix_id, timeout=timeout)

    @type_checker
    def expose(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        params = {
            "id": bitrix_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.expose),
            params=params,
            timeout=timeout,
        )
