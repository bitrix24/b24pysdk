from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from ..._field import Field
from .access import Access
from .chat import Chat
from .file import File
from .gantt import Gantt
from .result import Result

__all__ = [
    "Task",
]


class Task(BaseEntity):
    """Class for working with tasks in RESTv3.0.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @cached_property
    def chat(self) -> Chat:
        """"""
        return Chat(self)

    @cached_property
    def file(self) -> File:
        """"""
        return File(self)

    @cached_property
    def gantt(self) -> Gantt:
        """"""
        return Gantt(self)

    @cached_property
    def result(self) -> Result:
        """"""
        return Result(self)

    @cached_property
    def access(self) -> Access:
        """"""
        return Access(self)

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-add-rest-v3.html

        The method adds a new task.

        Args:
            fields: Values of task fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-delete-rest-v3.html

        The method removes task.

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
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get task by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-get-rest-v3.html

        The method returns information about a task by its identifier.

        Args:
             bitrix_id: Task identifier;

             select: List of fields to return;

             timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[Iterable] = MISSING,
            order: Optional[JSONDict] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get task list

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-list-rest-v3.html

        The method returns a list of tasks based on the specified conditions.

        Args:
            select: List of fields to return;

            filter: Task filtering conditions;

            order: Sorting of the result;

            pagination: Pagination parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not MISSING:
            if filter.__class__ is not list:
                filter = list(filter)

            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
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
        """Update task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-update-rest-v3.html

        The method updates task.

        Args:
            bitrix_id: Task identifier;

            fields: Values of task fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

