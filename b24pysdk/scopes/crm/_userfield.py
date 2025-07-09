from typing import TYPE_CHECKING, Optional, Union

from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, JSONList, Timeout
from .base_crm import BaseCRM

if TYPE_CHECKING:
    from . import Company, Contact, Deal, Lead, Quote, Requisite


class Userfield(BaseCRM):
    """"""

    def __init__(self, item: Union["Company", "Contact", "Deal", "Lead", "Quote", "Requisite"]):
        super().__init__(item._scope)
        self._path = self._get_path(item)

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
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._list(
            filter=filter,
            order=order,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            list: Optional[JSONList] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        if list is not None:
            params["LIST"] = list

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._update),
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
        return self._delete(bitrix_id, timeout=timeout)
