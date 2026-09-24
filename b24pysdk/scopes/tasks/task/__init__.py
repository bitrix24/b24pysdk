from functools import cached_property
from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .counters import Counters
from .favorite import Favorite
from .files import Files
from .gantt import Gantt
from .history import History
from .result import Result

__all__ = [
    "Task",
]


class Task(BaseEntity):
    """Class for working with tasks in Bitrix24.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @cached_property
    def counters(self) -> Counters:
        """"""
        return Counters(self)

    @cached_property
    def favorite(self) -> Favorite:
        """"""
        return Favorite(self)

    @cached_property
    def files(self) -> Files:
        """"""
        return Files(self)

    @cached_property
    def gantt(self) -> Gantt:
        """"""
        return Gantt(self)

    @cached_property
    def history(self) -> History:
        """"""
        return History(self)

    @cached_property
    def result(self) -> Result:
        """"""
        return Result(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-add.html

        The method adds a new task.

        Args:
            fields: Fields for creating a task;

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
    def approve(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Approve task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-approve.html

        The method accepts the work of the Participant on the task when task control is enabled and changes the task status to Completed.

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
            api_wrapper=self.approve,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def complete(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move task to completed

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/status/tasks-task-complete.html

        The method moves the task to the Completed status.

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
            api_wrapper=self.complete,
            params=params,
            timeout=timeout,
        )

    def delete(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-delete.html

        The method deletes a task.

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
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delegate(
            self,
            task_id: int,
            user_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delegate task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-delegate.html

        The method changes the responsible person and delegates the task to another user.

        Args:
            task_id: Task identifier;

            user_id: User identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "taskId": task_id,
            "userId": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delegate,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def disapprove(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Disapprove task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-disapprove.html

        The method disapproves a task and returns it for revision to the Participant when task control is enabled.

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
            api_wrapper=self.disapprove,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def defer(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Defer a task to the status "Deferred"

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/status/tasks-task-defer.html

        The method changes the task status to "Deferred."

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
            api_wrapper=self.defer,
            params=params,
            timeout=timeout,
        )

    def get(
            self,
            task_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get task by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-get.html

        The method returns information about a task by its ID.

        Args:
            task_id: Task identifier;

            select: An array of record fields that will be returned by the method;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "taskId": task_id,
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
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of fields

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-get-fields.html

        The method returns a description of standard and custom fields of a task.

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
    def getaccess(
            self,
            task_id: int,
            *,
            users: Optional[Iterable[int]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check access to task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-get-access.html

        The method checks the available actions for users on a task.

        Args:
            task_id: Task identifier;

            users: An array of user IDs for whom access needs to be checked;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "taskId": task_id,
        }

        if users is not MISSING:
            if users.__class__ is not list:
                users = list(users)

            params["users"] = users

        return self._make_bitrix_api_request(
            api_wrapper=self.getaccess,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            order: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            params: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get task list

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-list.html

        The method a list of tasks with pagination.

        Args:
            order: An object for sorting the task list;

            filter: An object for filtering the task list;

            select: An array containing a list of fields to select.

            params: Additional information that can be retrieved about the task;

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        _params: JSONDict = {}

        if order is not MISSING:
            _params["order"] = order

        if filter is not MISSING:
            _params["filter"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            _params["select"] = select

        if params is not MISSING:
            _params["params"] = params

        if start is not MISSING:
            _params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=_params,
            timeout=timeout,
        )

    @type_checker
    def mute(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Enable "Mute" mode

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-actions/tasks-task-mute.html

        The method enables "Mute" mode for a task.

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
            api_wrapper=self.mute,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def pause(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Translate the task to the Waiting for execution status

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/status/tasks-task-pause.html

        The method stops the execution of the task and changes its status to Waiting for Execution.

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
            api_wrapper=self.pause,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def pin(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Pin a task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-actions/tasks-task-pin.html

        The method pins a task in the current user's task list.

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
            api_wrapper=self.pin,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def renew(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Renew a task after completion

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/status/tasks-task-renew.html

        The method renews a task after it has been completed.

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
            api_wrapper=self.renew,
            params=params,
            timeout=timeout,
        )

    def start(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move task to In progress status

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/status/tasks-task-start.html

        The method moves the task to the In Progress status.

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
            api_wrapper=self.start,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def startwatch(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Enable task watching

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-actions/tasks-task-start-watch.html

        The method enables watching a task.

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
            api_wrapper=self.startwatch,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def stopwatch(
            self,
            task_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Disable task monitoring

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-actions/tasks-task-stop-watch.html

        The method disables monitoring for the task.

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
            api_wrapper=self.stopwatch,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpin(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Unpin a task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-actions/tasks-task-unpin.html

        The method unpins a task in the current user's task list.

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
            api_wrapper=self.unpin,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unmute(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Disable "Mute" mode

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/user-actions/tasks-task-unmute.html

        The method disables the "Mute" mode for a task.

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
            api_wrapper=self.unmute,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            task_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-update.html

        The method updates a task.

        Args:
            task_id: Task identifier;

            fields: Task fields to update;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "taskId": task_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
