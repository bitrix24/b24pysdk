from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Elapseditem",
]


class Elapseditem(BaseEntity):
    """A set of methods for working with time tracking in tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/elapsed-item/index.html
    """

    @type_checker
    def add(
            self,
            task_id: int,
            arfields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add elapsed time record

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/elapsed-item/task-elapsed-item-add.html

        The method adds elapsed time to a task. The identifier of the added record is returned.

        Args:
            task_id: Task identifier;

            arfields: An object containing records about the user, time, and comments;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ARFIELDS": arfields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            task_id: int,
            item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete time entry

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/elapsed-item/task-elapsed-item-delete.html

        The method deletes a time entry.

        Args:
            task_id: Task identifier;

            item_id: Time entry identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            task_id: int,
            item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get time entry by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/elapsed-item/task-elapsed-item-get.html

        The method returns a time entry by its ID.

        Args:
            task_id: Task identifier;

            item_id: Time entry identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getlist(
            self,
            *,
            task_id: Optional[int] = MISSING,
            order: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of time tracking records

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/elapsed-item/task-elapsed-item-get-list.html

        The method returns a list of time tracking records for a task.

        Args:
            task_id: Task identifier;

            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

            filter: Object for filtering the result;

            select: Array of fields of records that will be returned by the method;

            params: Object for call options;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        payload = dict()

        if task_id is not MISSING:
            payload["TASKID"] = task_id

        if order is not MISSING:
            payload["ORDER"] = order

        if filter is not MISSING:
            payload["FILTER"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            payload["SELECT"] = select

        if params is not MISSING:
            payload["PARAMS"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=payload,
            timeout=timeout,
        )

    @type_checker
    def getmanifest(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of methods and their descriptions

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/elapsed-item/task-elapsed-item-get-manifest.html

        The method returns a list of methods and their descriptions.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.getmanifest,
            timeout=timeout,
        )

    @type_checker
    def isactionallowed(
            self,
            task_id: int,
            item_id: int,
            action_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check action permission

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/elapsed-item/task-elapsed-item-is-action-allowed.html

        The method checks whether an action is permitted for a record: creation, update, and deletion.

        Args:
            task_id: Task identifier;

            item_id: Time entry identifier;

            action_id: Action identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
            "ACTIONID": action_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.isactionallowed,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            task_id: int,
            item_id: int,
            arfields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update time entry

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/elapsed-item/task-elapsed-item-update.html

        The method updates the parameters of the specified time entry.

        Args:
            task_id: Task identifier;

            item_id: Time entry identifier;

            arfields: An object containing records about the user, time, and comments;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
            "ARFIELDS": arfields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
