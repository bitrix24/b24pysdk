from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Planner",
]


class Planner(BaseEntity):
    """Class for collecting tasks, sctivities and meetings that need to be completed.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/planner/index.html
    """

    @type_checker
    def getlist(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of tasks from the daily plan

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/planner/task-planner-get-list.html

        The method retrieves a list of task identifiers from the current user's "Daily Plan."

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            timeout=timeout,
        )
