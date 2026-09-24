from typing import Optional

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Checklistitem",
]


class Checklistitem(BaseEntity):
    """Class for working with checklists in tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/index.html
    """

    @type_checker
    def add(
            self,
            task_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add checklist item

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-add.html

        The method adds a new checklist item to a task.

        Args:
            task_id: Task identifier;

            fields: Object with checklist item fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def complete(
            self,
            task_id: int,
            item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Mark a checklist item as completed

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-complete.html

        The method marks a checklist item as completed.

        Args:
            task_id: Task identifier;

            item_id: Checklist item identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.complete,
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
        """Delete checklist item

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-delete.html

        The method removes a checklist item from a task.

        Args:
            task_id: Task identifier;

            item_id: Checklist item identifier;

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
        """Get checklist item

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-get.html

        The method retrieves the description of a checklist item by its identifier.

        Args:
            task_id: Task identifier;

            item_id: Checklist item identifier;

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
            task_id: int,
            *,
            order: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of checklist items

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-get-list.html

        The method retrieves a list of checklist items in a task.

        Args:
            task_id: Task identifier;

            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
        }

        if order is not MISSING:
            params["ORDER"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getmanifest(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of methods and their description

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-get-manifest.html

        The method retrieves information about methods for working with task checklist items.

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

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-is-action-allowed.html

        The method checks whether an action is permitted for a checklist item in a task.

        Args:
            task_id: Task identifier;

            item_id: Checklist item identifier;

            action_id: Identifier of the action being checked;

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
    def moveafteritem(
            self,
            task_id: int,
            item_id: int,
            after_item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move checklist item

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-move-after-item.html

        The method moves the checklist item itemId to a position after the element afterItemId.

        Args:
            task_id: Task identifier;

            item_id: Checklist item identifier;

            after_item_id: Identifier of the checklist item after which the moving item should be placed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
            "AFTERITEMID": after_item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.moveafteritem,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def renew(
            self,
            task_id: int,
            item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Mark a checklist item as incomplete

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-renew.html

        The method marks a completed checklist item as incomplete.

        Args:
            task_id: Task identifier;

            item_id: Checklist item identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.renew,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            task_id: int,
            item_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update checklist item

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/checklist-item/task-checklist-item-update.html

        The method modifies an existing checklist item.

        Args:
            task_id: Task identifier;

            item_id: Checklist item identifier;

            fields: Fields to update;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
            "ITEMID": item_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
