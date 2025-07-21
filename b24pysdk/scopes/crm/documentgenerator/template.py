from typing import TYPE_CHECKING, Iterable, Optional, Text

from ....bitrix_api.classes.bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .documentgenerator import Documentgenerator


class Template(BaseCRM):
    """The method offer capabilities for working with document templates.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/templates/index.html
    """

    def __init__(self, documentgenerator: "Documentgenerator"):
        super().__init__(documentgenerator._scope)
        self._path = self._get_path(documentgenerator)

    @type_checker
    def getfields(
            self,
            bitrix_id: int,
            *,
            entity_type_id: int,
            entity_id: Optional[int] = None,
            values: Optional[JSONList] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get document template fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/templates/crm-document-generator-template-get-fields.html

        The method returns a list of template fields along with their descriptions.

        Args:
            bitrix_id: Identifier of the template;

            entity_type_id: Identifier of the CRM entity type;

            entity_id: Identifier of the entity being used;

            values: Array of additional values;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "entityTypeId": entity_type_id,
        }

        if entity_id is not None:
            params["entityId"] = entity_id,

        if values is not None:
            params["values"] = values

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.getfields),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a new template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/templates/crm-document-generator-template-add.html

        The method adds a new template.

        Args:
            fields: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields=fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get documentation template information by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/templates/crm-document-generator-template-get.html

        The method returns information about a template by its identifier.

        Args:
            bitrix_id: Template ID;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id=bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of document templates.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/templates/crm-document-generator-template-list.html

        The method returns a list of templates based on the filter.

        Args:
            select: Array of fields to output;

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            filter: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(
            select=select,
            order=order,
            filter=filter,
            start=start,
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
        """Update existing document template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/templates/crm-document-generator-template-update.html

        The method updates an existing template.

        Args:
            bitrix_id: Template identifier;

            fields: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(
            bitrix_id=bitrix_id,
            fields=fields,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete document template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/templates/crm-document-generator-template-delete.html

        The method deletes a template.

        Args:
            bitrix_id: Template identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id=bitrix_id, timeout=timeout)
