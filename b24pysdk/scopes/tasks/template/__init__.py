from functools import cached_property

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .checklist import Checklist

__all__ = [
    "Template",
]


class Template(BaseEntity):
    """Class for managing task templates.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/index.html
    """

    @cached_property
    def checklist(self) -> Checklist:
        """"""
        return Checklist(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/tasks-template-add.html

        The method creates a new task template.

        Args:
            fields: Fields of new task template;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
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
            template_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/tasks-template-delete.html

        The method removes a task template.

        Args:
            template_id: ID of task template;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/tasks-template-fields.html

        The method returns the description of the task template fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            template_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get task template by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/tasks-template-get.html

        The method returns the task template data by its ID.

        Args:
            template_id: ID of task template;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            template_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update task template

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/template/tasks-template-update.html

        The method updates an existing task template.

        Args:
            template_id: ID of task template;

            fields: The fields of the template that need to be changed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "templateId": template_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
