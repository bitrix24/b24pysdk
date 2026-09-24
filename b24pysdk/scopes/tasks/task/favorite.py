from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Favorite",
]


class Favorite(BaseEntity):
    """Class for managing tasks in Favorites.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @type_checker
    def add(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add task to Favorites

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-actions/tasks-task-favorite-add.html

        The method adds a task to Favorites.

        Args:
            task_id: Task identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def remove(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove task from Favorites

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-actions/tasks-task-favorite-remove.html

        The method removes a task from Favorites.

        Args:
            task_id: Task identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "taskId": task_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.remove,
            params=params,
            timeout=timeout,
        )
