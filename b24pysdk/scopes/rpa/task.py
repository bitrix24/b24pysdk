from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Task",
]


class Task(BaseEntity):
    """"""

    @type_checker
    def add_user(
            self,
            *,
            type_id: Optional[int] = MISSING,
            stage_id: Optional[int] = MISSING,
            robot_name: Optional[Text] = MISSING,
            user_value: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if type_id is not MISSING:
            params["typeId"] = type_id

        if stage_id is not MISSING:
            params["stageId"] = stage_id

        if robot_name is not MISSING:
            params["robotName"] = robot_name

        if user_value is not MISSING:
            params["userValue"] = user_value

        return self._make_bitrix_api_request(
            api_wrapper=self.add_user,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            type_id: int,
            stage_id: int,
            robot_name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "typeId": type_id,
            "stageId": stage_id,
            "robotName": robot_name,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def do(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.do,
            timeout=timeout,
        )
