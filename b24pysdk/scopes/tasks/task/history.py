from typing import Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "History",
]


class History(BaseEntity):
    """Class for retrieving task history.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @type_checker
    def list(
            self,
            task_id: int,
            *,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get task history

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-history-list.html

        The method retrieves the history of changes for a task.

        Args:
            task_id: The identifier of the task for which the history needs to be retrieved;

            filter: Filter by event type;

            order: An object for sorting the result;

            start: Parameter for managing pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "taskId": task_id,
        }

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
