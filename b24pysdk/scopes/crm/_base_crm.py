from abc import ABC
from typing import Callable, Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest
from ...schemas.crm.field import CRMFieldsDict
from ...utils.type_vars import BAResultT, BAValueT
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "BaseCRM",
]


class BaseCRM(BaseEntity, ABC):
    """"""

    def _fields(
            self,
            *,
            timeout: Timeout = None,
            result_adapter: Callable[[BAResultT], BAValueT] = CRMFieldsDict.from_bitrix,
    ) -> BitrixAPIValueRequest[BAResultT, BAValueT]:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self._fields,
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
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        if start is not None:
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
