from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, JSONList, Timeout
from ...._base_entity import BaseEntity
from ..._field import Field

__all__ = [
    "Result",
]


class Result(BaseEntity):
    """Class for managing task results.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/index.html
    """

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
    ) -> BitrixAPIRequest[JSONDict]:
        """Add result to task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/tasks-task-result-add.html

        The method adds a result to a task.

        Args:
            fields: Object with result fields;

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
    def addfromchatmessage(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Add result from task chat message

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/tasks-task-result-addfromchatmessage.html

        The method creates a task result from a task chat message.

        Args:
            fields: Object with result fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.addfromchatmessage,
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
    ) -> BitrixAPIRequest[JSONDict]:
        """Update task result

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/tasks-task-result-update.html

        The method updates the text of the task result.

        Args:
            bitrix_id: Identifier of the result;

            fields: Object with result fields;

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

    @type_checker
    def list(
            self,
            filter: Iterable[Iterable],
            *,
            order: Optional[JSONDict] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """Get task result list

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/tasks-task-result-list-rest-v3.html

        The method returns a list of task results.

        Args:
            filter: An array of conditions for filtering the list of results;

            order: An object for sorting the list of results in the format;

            select: An array of fields to select;

            pagination: An object for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if filter.__class__ is not list:
            filter = list(filter)

        params = {
            "filter": filter,
        }

        if order is not MISSING:
            params["order"] = order

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Delete task result

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/result/tasks-task-result-delete.html

        The method deletes the task result.

        Args:
            bitrix_id: Identifier of the result;

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
