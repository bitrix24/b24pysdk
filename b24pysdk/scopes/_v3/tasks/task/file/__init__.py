from functools import cached_property
from typing import Iterable

from ......api.requests import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import Timeout
from ....._base_entity import BaseEntity
from ...._field import Field

__all__ = [
    "File",
]


class File(BaseEntity):
    """Class for attaching files to tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def attach(
            self,
            task_id: int,
            file_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Attach files to a task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-file-attach.html

        The method adds files from Drive to a task.

        Args:
            task_id: Task identifier;

            file_ids: An array of file identifiers from Drive;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if file_ids.__class__ is not list:
            file_ids = list(file_ids)

        params = {
            "taskId": task_id,
            "fileIds": file_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.attach,
            params=params,
            timeout=timeout,
        )
