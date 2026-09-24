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
    """A set of methods for working with tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/task/index.html
    """

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
        """Add user to existing task

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/task/rpa-task-add-user.html

        The method will add a user to an existing task.

        Args:
            type_id: Process identifier;

            stage_id: Stage identifier;

            robot_name: Name of the Automation rule;

            user_value: String with user in the format First Last [user ID]

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Remove Automation rule

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/task/rpa-task-delete.html

        This method removes the Automation rule named robotName from the process with the identifier typeId at the stage with the identifier stageId.

        Args:
            type_id: Identifier of the process;

            stage_id: Stage identifier;

            robot_name: Name of the automation rule;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Execute the command

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/task/rpa-task-do.html

        This method executes a task.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.do,
            timeout=timeout,
        )
