from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Kanban",
]


class Kanban(BaseEntity):
    """"""

    @type_checker
    def add_stage(
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
            api_wrapper=self.add_stage,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add_task(
            self,
            sprint_id: int,
            task_id: int,
            stage_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "sprintId": sprint_id,
            "taskId": task_id,
            "stageId": stage_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add_task,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_stage(
            self,
            stage_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "stageId": stage_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_stage,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_task(
            self,
            sprint_id: int,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "sprintId": sprint_id,
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_task,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def get_stages(
            self,
            sprint_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "sprintId": sprint_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_stages,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_stage(
            self,
            stage_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "stageId": stage_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update_stage,
            params=params,
            timeout=timeout,
        )
