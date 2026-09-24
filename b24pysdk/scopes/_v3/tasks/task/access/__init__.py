from functools import cached_property

from ......api.requests import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import Timeout
from ....._base_entity import BaseEntity
from ...._field import Field

__all__ = [
    "Access",
]


class Access(BaseEntity):
    """Class for checking access permissions.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check access permissions

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-access-get.html

        The method checks the available actions a user can perform on a task.

        Args:
            bitrix_id: Task identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
