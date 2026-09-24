from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Dependence",
]


class Dependence(BaseEntity):
    """Class for managing dependencies between tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @type_checker
    def add(
            self,
            task_id_from: int,
            task_id_to: int,
            link_type: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a link between tasks

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/task-dependence-add.html

        This method creates a dependency of one task on another.

        Args:
            task_id_from: Identifier of the task from which the dependency is created;

            task_id_to: Identifier of the task for which the dependency is created;

            link_type: Type of dependency;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "taskIdFrom": task_id_from,
            "taskIdTo": task_id_to,
            "linkType": link_type,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            task_id_from: int,
            task_id_to: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove dependency between tasks

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/task-dependence-delete.html

        This method removes the dependency of one task on another.

        Args:
            task_id_from: Identifier of the task from which the dependency is removed;

            task_id_to: Identifier of the task for which the dependency is removed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "taskIdFrom": task_id_from,
            "taskIdTo": task_id_to,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
