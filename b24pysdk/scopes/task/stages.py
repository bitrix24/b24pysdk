from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Stages",
]


class Stages(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            is_admin: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "fields": fields,
        }

        if is_admin is not None:
            params["isAdmin"] = is_admin

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def canmovetask(
            self,
            entity_id: int,
            entity_type: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityId": entity_id,
            "entityType": entity_type,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.canmovetask,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            is_admin: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if is_admin is not None:
            params["isAdmin"] = is_admin

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            entity_id: int,
            *,
            is_admin: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "entityId": entity_id,
        }

        if is_admin is not None:
            params["isAdmin"] = is_admin

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def movetask(
            self,
            bitrix_id: int,
            stage_id: int,
            *,
            before: Optional[int] = None,
            after: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "stageId": stage_id,
        }

        if before is not None:
            params["before"] = before

        if after is not None:
            params["after"] = after

        return self._make_bitrix_api_request(
            api_wrapper=self.movetask,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            is_admin: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        if is_admin is not None:
            params["isAdmin"] = is_admin

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
