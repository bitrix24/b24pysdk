from typing import Iterable, Optional, Sequence, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24File, DocumentType, JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Template",
]


class Template(BaseEntity):
    """Handle operations related to Bitrix24 bizproc workflow templates.

    Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/template/index.html
    """

    @type_checker
    def add(
            self,
            document_type: Sequence[Text],
            name: Text,
            template_data: Sequence[Text],
            *,
            description: Optional[Text] = None,
            auto_execute: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a workflow template from a .bpt file.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/template/bizproc-workflow-template-add.html

        This method works only in the application context and binds the template to the application.

        Args:
            document_type: Array of three strings that defines the document type to which the template will be attached;
            name: Template name;
            template_data: File content for the workflow template in .bpt format;
            description: Template description;
            auto_execute: Auto start settings: 0 — no auto start, 1 — on create, 2 — on update, 3 — on create and update;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        params = {
            "DOCUMENT_TYPE": DocumentType(document_type).to_b24(),
            "NAME": name,
            "TEMPLATE_DATA": B24File(template_data).to_b24(),
        }

        if description is not None:
            params["DESCRIPTION"] = description

        if auto_execute is not None:
            params["AUTO_EXECUTE"] = auto_execute

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
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
        """Update a workflow template.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/template/bizproc-workflow-template-update.html

        Only templates created via bizproc.workflow.template.add can be updated, and only in the same application context. Only the fields NAME, DESCRIPTION, TEMPLATE_DATA, and AUTO_EXECUTE can be updated; other fields will be ignored without an error.

        Args:
            bitrix_id: Identifier of the workflow template to update;
            fields: Object format:
                {
                    "NAME": "value",

                    "DESCRIPTION": "value",

                    "TEMPLATE_DATA": ["file name", "file content"],

                    "AUTO_EXECUTE": integer
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ID": bitrix_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

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
        """Retrieve a list of workflow templates.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/template/bizproc-workflow-template-list.html

        The result supports pagination with a fixed page size of 50. To fetch page N, pass start = (N - 1) * 50. By default, SELECT is ['ID'] and ORDER is {ID: 'ASC'}.

        Args:
            select: List of fields to select; defaults to ['ID'] if not provided;
            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
                }

                - field_n is the field used for filtering,

                - value_n is field value;

            order: Object format:
                {
                    field_1: value_1,

                    ...,

                    field_n: value_n,
                }

                where

                - field_n is the field used for sorting,

                - value_n is either 'asc' (ascending) or 'desc' (descending);
            start: Offset for pagination; pass 0 for the first page, 50 for the second, and so on;
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
            params["start"] = start

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
    ) -> BitrixAPIRequest:
        """Delete a workflow template.

        Documentation: https://apidocs.bitrix24.com/api-reference/bizproc/template/bizproc-workflow-template-delete.html

        Only templates created via bizproc.workflow.template.add can be deleted, and only in the same application context.

        Args:
            bitrix_id: Identifier of the workflow template to delete;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
