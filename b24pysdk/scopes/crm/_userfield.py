from typing import Optional, TYPE_CHECKING, Union

from ..._bitrix_api_request import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, JSONList

from .base_crm import BaseCRM

if TYPE_CHECKING:
    from . import Company, Contact, Deal, Lead


class Userfield(BaseCRM):
    """"""

    def __init__(self, item: Union["Company", "Contact", "Deal", "Lead"]):
        super().__init__(item._scope)
        self._path = self._get_path(item)

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
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            timeout: Optional[int] = None,
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
            timeout: Optional[int] = None,
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

    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._delete(bitrix_id, timeout=timeout)
