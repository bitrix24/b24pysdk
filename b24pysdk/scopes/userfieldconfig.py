from typing import Optional, Text

from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Userfieldconfig",
]


class Userfieldconfig(BaseScope):
    """"""

    @type_checker
    def add(
            self,
            module_id: Text,
            field: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "moduleId": module_id,
            "field": field,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            module_id: Text,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "moduleId": module_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            module_id: Text,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "moduleId": module_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_types(
            self,
            module_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "moduleId": module_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_types,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            module_id: Text,
            *,
            select: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "moduleId": module_id,
        }

        optional_params = {
            "select": select,
            "order": order,
            "filter": filter,
            "start": start,
        }

        if optional_params.get("select") is not None:
            params["select"] = optional_params.get("select")

        if optional_params.get("order") is not None:
            params["order"] = optional_params.get("order")

        if optional_params.get("filter") is not None:
            params["filter"] = optional_params.get("filter")

        if optional_params.get("start") is not None:
            params["start"] = optional_params.get("start")

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            module_id: Text,
            bitrix_id: int,
            *,
            field: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "moduleId": module_id,
            "id": bitrix_id,
        }

        if field is not None:
            params["field"] = field

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
