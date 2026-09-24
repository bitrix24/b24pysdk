from typing import Optional

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Commentitem",
]


class Commentitem(BaseEntity):
    """Class for managing comments in tasks.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/comment-item/index.html
    """

    @type_checker
    def add(
            self,
            task_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add comment

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/comment-item/task-comment-item-add.html

        The method adds a comment to a task.

        Args:
            task_id: Task identifier;

            fields: Object with comment fields;

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
    def delete(
            self,
            task_id: int,
            item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete comment

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/comment-item/task-comment-item-delete.html

        The method deletes a comment.

        Args:
            task_id: Task identifier;

            item_id: Comment identifier;

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
        """Get comment by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/comment-item/task-comment-item-get.html

        The method retrieves a comment by its ID.

        Args:
            task_id: Task identifier;

            item_id: Comment identifier;

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
            filter: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of comments

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/comment-item/task-comment-item-get-list.html

        The method retrieves a list of task comments.

        Args:
            task_id: Task identifier;

            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

            filter: An object for filtering the result;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "TASKID": task_id,
        }

        if order is not MISSING:
            params["ORDER"] = order

        if filter is not MISSING:
            params["FILTER"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
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
        """Update comment

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/comment-item/task-comment-item-update.html

        The method updates comment data.

        Args:
            task_id: Task identifier;

            item_id: Comment identifier;

            fields: Comment fields to update;

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
