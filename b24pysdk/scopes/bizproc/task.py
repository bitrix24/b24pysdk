from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Task",
]


class Task(BaseEntity):
    """Handle operations related to Bitrix24 business process tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-task/index.html
    """

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve a list of business process tasks.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-task/bizproc-task-list.html

        Administrators can request all tasks or tasks of any user. A regular user can request their own tasks or the tasks of their subordinates. The result set is paginated with a fixed page size of 50.

        Args:
            select: Array of fields to return;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }, where if USER_ID is present, subordination is checked: a manager may request tasks of subordinates; if the caller is not an administrator and USER_ID is not specified, tasks of the current user are selected by default;

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                    where

                    - field_n is the task field to sort by;

                    - value_n is 'asc' for ascending or 'desc' for descending; multiple fields can be specified;

            start: Offset for page navigation;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = dict()

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["SELECT"] = select

        if filter is not None:
            params["FILTER"] = filter

        if order is not None:
            params["ORDER"] = order

        if start is not None:
            params["START"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def complete(
            self,
            task_id: int,
            status: Union[Text, int],
            *,
            comment: Optional[Text] = None,
            fields: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Complete a business process task.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-task/bizproc-task-complete.html

        Use this to perform approval, acknowledgment, request for additional information, or request for information with rejection.

        Only your own tasks can be completed. Allowed status values depend on the task type.

        Args:
            task_id: Identifier of the task;

            status: Target status of the task;

            comment: User comment; whether it is required depends on task settings;

            fields: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }, where field_N is the symbolic identifier of a task field and value_N is its value;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "TASK_ID": task_id,
            "STATUS": status,
        }

        if comment is not None:
            params["COMMENT"] = comment

        if fields is not None:
            params["FIELDS"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.complete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delegate(
            self,
            task_ids: Iterable[int],
            from_user_id: int,
            to_user_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Delegate business process tasks to another user.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/bizproc-task/bizproc-task-delegate.html

        This method delegates a workflow task. You can only delegate your own task.

        Args:
            task_ids: List of task identifiers to delegate;

            from_user_id: Identifier of the current assignee;

            to_user_id: Identifier of the new assignee;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if task_ids.__class__ is not list:
            task_ids = list(task_ids)

        params = {
            "TASK_IDS": task_ids,
            "FROM_USER_ID": from_user_id,
            "TO_USER_ID": to_user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delegate,
            params=params,
            timeout=timeout,
        )
