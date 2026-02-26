from typing import Optional

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Checklistitem",
]


class Checklistitem(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            task_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def complete(
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
            api_wrapper=self.complete,
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
            task_id: int,
            *,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
        }

        if order is not None:
            params["ORDER"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=params,
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
    def moveafteritem(
            self,
            task_id: int,
            item_id: int,
            after_item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
            "AFTERITEMID": after_item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.moveafteritem,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def renew(
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
            api_wrapper=self.renew,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            task_id: int,
            item_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
