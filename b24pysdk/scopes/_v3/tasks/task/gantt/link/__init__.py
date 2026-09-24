from functools import cached_property
from typing import Iterable, Text

from ......._constants import MISSING
from .......api.requests import BitrixAPIRequest
from .......utils.functional import type_checker
from .......utils.types import JSONDict, Timeout
from ......_base_entity import BaseEntity
from ....._field import Field

__all__ = [
    "Link",
]


class Link(BaseEntity):
    """Class for retrieving Gantt links for tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def list(
            self,
            filter: Iterable,
            *,
            select: Iterable[Text] = MISSING,
            pagination: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get task Gantt link list

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-gantt-link-list.html

        The method returns a list of outgoing Gantt links for a task.

        Args:
            filter: Filter for selecting links of a task;

            select: Array of fields to return;

            pagination: Object for managing pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if not isinstance(filter, list):
            filter = list(filter)

        params: JSONDict = {
            "filter": filter,
        }

        if select is not MISSING:
            if not isinstance(select, list):
                select = list(select)

            params["select"] = select

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
