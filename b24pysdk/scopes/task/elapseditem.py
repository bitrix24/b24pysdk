from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Elapseditem",
]


class Elapseditem(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            task_id: int,
            arfields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
            "ARFIELDS": arfields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            task_id: int,
            item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            task_id: int,
            item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getlist(
            self,
            *,
            task_id: Optional[int] = None,
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        payload = dict()

        if task_id is not None:
            payload["TASKID"] = task_id

        if order is not None:
            payload["ORDER"] = order

        if filter is not None:
            payload["FILTER"] = filter

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            payload["SELECT"] = select

        if params is not None:
            payload["PARAMS"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=payload,
            timeout=timeout,
        )

    @type_checker
    def getmanifest(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.getmanifest,
            timeout=timeout,
        )

    @type_checker
    def isactionallowed(
            self,
            task_id: int,
            item_id: int,
            action_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
            "ACTIONID": action_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.isactionallowed,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            task_id: int,
            item_id: int,
            arfields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
            "ARFIELDS": arfields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
