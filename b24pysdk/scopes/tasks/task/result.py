from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Result",
]


class Result(BaseEntity):
    """Class for managing task results.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/index.html
    """

    @type_checker
    def add_from_comment(
            self,
            comment_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add comment to result

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/tasks-task-result-add-from-comment.html

        The method pins a comment as the result of task execution.

        Args:
            comment_id: The identifier of the comment to be pinned as a result;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "commentId": comment_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add_from_comment,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete_from_comment(
            self,
            comment_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove comment from result

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/tasks-task-result-delete-from-comment.html

        The method unpins a comment as the result of a task.

        Args:
            comment_id: The identifier of the comment for which the result needs to be unpinned;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "commentId": comment_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_from_comment,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of task results

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/tasks-task-result-list.html

        The method retrieves a list of results associated with a task.

        Args:
            task_id: The identifier of the task from which to retrieve results;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
