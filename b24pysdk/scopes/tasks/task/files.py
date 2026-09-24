from typing import Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Files",
]


class Files(BaseEntity):
    """Class for attaching files to tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @type_checker
    def attach(
            self,
            task_id: int,
            file_id: int,
            *,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Attach files to a task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-files-attach.html

        The method adds a file from Drive to a task.

        Args:
            task_id: The identifier of the task to which the file needs to be attached;

            file_id: The identifier of the file on Drive;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        payload = {
            "taskId": task_id,
            "fileId": file_id,
        }

        if params is not MISSING:
            payload["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.attach,
            params=payload,
            timeout=timeout,
        )
