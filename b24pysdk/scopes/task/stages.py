from typing import Annotated, Literal, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Stages",
]


class Stages(BaseEntity):
    """Class for managing stages of Kanban and "My planner".

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/stages/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            is_admin: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a Kanban or "My plan" stage

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/stages/task-stages-add.html

        The method adds a Kanban or "My Plan" stage.

        Args:
            fields: Field values for adding a new stage;

            is_admin: If set to true, permission checks will not occur, provided the requester is an administrator of the account;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        if is_admin is not MISSING:
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
            entity_type: Annotated[Text, Literal["U", "G"]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check the ability to move task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/stages/task-stages-can-move-task.html

        The method checks whether the current user can move tasks in the specified object.

        Args:
            entity_id: ID of the object;

            entity_type: Type of the object;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
            is_admin: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete a Kanban or "My plan" stage

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/stages/task-stages-delete.html

        The method deletes a Kanban or "My Plan" stage.

        Args:
            bitrix_id: Identifier of the stage to be deleted;

            is_admin: If set to true, permission checks will be skipped, provided the requester is an administrator of the account;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        if is_admin is not MISSING:
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
            is_admin: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of Kanban stages or "My plan"

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/stages/task-stages-get.html

        The method task.stages.get retrieves Kanban stages or "My Plan" stages.

        Args:
            entity_id: Identifier of the object;

            is_admin: If set to true, permission checks will not occur, provided that the requester is an administrator of the account;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityId": entity_id,
        }

        if is_admin is not MISSING:
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
            before: Optional[int] = MISSING,
            after: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move task from one stage to another

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/stages/task-stages-move-task.html

        The method moves a task from one stage to another and allows you to change the task position within a group Kanban or "My Plan".

        Args:
            bitrix_id: Task identifier;

            stage_id: ID of the stage to which the task should be moved;

            before: ID of the task before which the task should be placed in the stage;

            after: ID of the task after which the task should be placed in the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "stageId": stage_id,
        }

        if before is not MISSING:
            params["before"] = before

        if after is not MISSING:
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
            is_admin: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update Kanban stage or "My plan"

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/stages/task-stages-update.html

        The method updates Kanban or "My Plan" stages.

        Args:
            bitrix_id: Identifier of the stage;

            fields: Field values for updating the stage;

            is_admin: If set to true, permission checks will not occur, provided the requester is an administrator of the account;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        if is_admin is not MISSING:
            params["isAdmin"] = is_admin

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
