from abc import ABC
from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest
from ...schemas.crm.field import CRMFieldsDict
from ...utils.type_vars import BSDataT, BSDictT
from ...utils.types import JSONDict, Timeout
from .._adapters import BitrixSchemaDictAdapter
from .._base_entity import BaseEntity

__all__ = [
    "CRM_FIELDS_DICT_ADAPTER",
    "BaseCRM",
]

CRM_FIELDS_DICT_ADAPTER = BitrixSchemaDictAdapter(CRMFieldsDict)


class BaseCRM(BaseEntity, ABC):
    """"""

    def _fields(
            self,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            result_adapter: BitrixSchemaDictAdapter[BSDataT, BSDictT] = CRM_FIELDS_DICT_ADAPTER,
    ) -> BitrixAPIValueRequest[BSDataT, BSDictT]:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self._fields,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=result_adapter,
        )

    def _add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self._add,
            params=params,
            timeout=timeout,
        )

    def _get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self._get,
            params=params,
            timeout=timeout,
        )

    def _list(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self._list,
            params=params,
            timeout=timeout,
        )

    def _update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self._update,
            params=params,
            timeout=timeout,
        )

    def _delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self._delete,
            params=params,
            timeout=timeout,
        )
