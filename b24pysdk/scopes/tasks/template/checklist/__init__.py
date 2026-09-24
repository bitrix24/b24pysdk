from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Checklist",
]


class Checklist(BaseEntity):
    """Class for managing task template checklists.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/index.html
    """

    @type_checker
    def add(
            self,
            template_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add checklist item to task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-add.html

        The method adds a checklist item to the task template.

        Args:
            template_id: Template identifier;

            fields: Fields of the created checklist item;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add_attachment_by_content(
            self,
            template_id: int,
            check_list_item_id: int,
            attachment_parameters: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add attachment to checklist item

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-add-attachment-by-content.html

        The method adds an attachment to a checklist item based on the content of a file.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier;

            attachment_parameters: Parameters of the created attachment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
            "attachmentParameters": attachment_parameters,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add_attachment_by_content,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add_attachments_from_disk(
            self,
            template_id: int,
            check_list_item_id: int,
            files_ids: Iterable[str],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add attachment from Drive to checklist item

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-add-attachments-from-disk.html

        The method adds files from Drive to a checklist item.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier;

            files_ids: An array of file identifiers from Drive;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if files_ids.__class__ is not list:
            files_ids = list(files_ids)

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
            "filesIds": files_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add_attachments_from_disk,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def complete(
            self,
            template_id: int,
            check_list_item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Complete checklist item of task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-complete.html

        The method marks a checklist item of the template as completed.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.complete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            template_id: int,
            check_list_item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete checklist item from task

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-delete.html

        The method removes a checklist item from the task template.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            template_id: int,
            check_list_item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get checklist item from task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-get.html

        The method returns a single checklist item from the task template.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            template_id: int,
            *,
            filter: Optional[JSONDict] = MISSING,
            select: Optional[Iterable[Text]] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of checklist items for task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-list.html

        The method returns a list of checklist items for the task template.

        Args:
            template_id: Template identifier;

            filter: Filter for selecting checklist items;

            select: List of fields to select;

            order: Object for sorting the result;

            start: Parameter for managing pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
        }

        if filter is not MISSING:
            params["filter"] = filter

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def move_after(
            self,
            template_id: int,
            check_list_item_id: int,
            after_item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move checklist item after another

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-move-after.html

        The method moves a checklist item after a specified item.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier to be moved;

            after_item_id: The identifier of the item after which the element should be place;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
            "afterItemId": after_item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.move_after,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def move_before(
            self,
            template_id: int,
            check_list_item_id: int,
            before_item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Move checklist item before another

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-move-before.html

        The method moves a checklist item before the specified item.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier to be moved;

            before_item_id: The identifier of the item before which the element should be place;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
            "beforeItemId": before_item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.move_before,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def remove_attachments(
            self,
            template_id: int,
            check_list_item_id: int,
            attachments_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove attachment from checklist item

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-remove-attachments.html

        The method removes attachments from a checklist item in the task template.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier;

            attachments_ids: Array of attachments identifier to be removed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if attachments_ids.__class__ is not list:
            attachments_ids = list(attachments_ids)

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
            "attachmentsIds": attachments_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.remove_attachments,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def renew(
            self,
            template_id: int,
            check_list_item_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Renew checklist item of task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-renew.html

        The method removes the completion mark from a checklist item of the task template.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.renew,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            template_id: int,
            check_list_item_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update checklist item of task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/checklist/tasks-template-checklist-update.html

        The method updates a checklist item of the task template.

        Args:
            template_id: Template identifier;

            check_list_item_id: Checklist item identifier;

            fields: Fields to update the checklist item;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "checkListItemId": check_list_item_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
