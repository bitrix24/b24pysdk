from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Task",
]


class Task(BaseEntity):
    """Class for managing Scrum tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/task/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get Scrum task

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/task/tasks-api-scrum-task-get.html

        This method retrieves the values of the Scrum task fields by its identifier id.

        Args:
            bitrix_id: Task identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get Scrum task fields

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/task/tasks-api-scrum-task-get-fields.html

        The method retrieves the available fields of a Scrum task.

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
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create or update Scrum task

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/scrum/task/tasks-api-scrum-task-update.html

        This method creates or updates a Scrum task.

        Args:
            bitrix_id: Task identifier;

            fields: An object containing records about the Scrum task;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
