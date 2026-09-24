from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Kanban",
]


class Kanban(BaseEntity):
    """Methods for working with Kanban in Scrum.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/kanban/index.html
    """

    @type_checker
    def add_stage(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a Scrum Kanban stage

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/kanban/tasks-api-scrum-kanban-add-stage.html

        This method creates a Scrum Kanban stage.

        Args:
            fields: Fields corresponding to the available list of fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Add task to Scrum Kanban

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/kanban/tasks-api-scrum-kanban-add-task.html

        This method adds a task to the Scrum Kanban.

        Args:
            sprint_id: Identifier of the sprint;

            task_id: Identifier of the task;

            stage_id: Identifier of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Delete stage

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/kanban/tasks-api-scrum-kanban-delete-stage.html

        This method deletes a stage.

        Args:
            stage_id: Identifier of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Delete task from Scrum Kanban

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/kanban/tasks-api-scrum-kanban-delete-task.html

        This method removes a task from the Scrum Kanban.

        Args:
            sprint_id: Sprint identifier;

            task_id: Identifier of the task;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Get a list of available fields for the Kanban stage

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/kanban/tasks-api-scrum-kanban-get-fields.html

        The method returns the available fields for the Kanban stage.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Get Kanban stages by sprint ID

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/kanban/tasks-api-scrum-kanban-get-stages.html

        The method returns the Kanban stages by the sprint ID.

        Args:
            sprint_id: Sprint identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Update Scrum Kanban stage

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/kanban/tasks-api-scrum-kanban-update-stage.html

        This method changes the stage of the Scrum Kanban.

        Args:
            stage_id: Identifier of the stage;

            fields: Fields corresponding to the available list of fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "stageId": stage_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update_stage,
            params=params,
            timeout=timeout,
        )
