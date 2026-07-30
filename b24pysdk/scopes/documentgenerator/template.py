from typing import Iterable, Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Template",
]


class Template(BaseEntity):
    """Methods help handle document generator templates.

    Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/templates/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Upload template

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/templates/document-generator-template-add.html

        The method adds a new document template.

        Args:
            fields: Set of template fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
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
        bitrix_id: Union[int, Text],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete template

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/templates/document-generator-template-delete.html

        The method removes a template.

        Args:
            bitrix_id: Identifier of the template;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
        self,
        bitrix_id: Union[int, Text],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get template by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/templates/document-generator-template-get.html

        The method returns information about a template by its ID.

        Args:
            bitrix_id: Identifier of the template;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getfields(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of fields

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/templates/document-generator-template-get-fields.html

        The method returns the detail form of the template fields.

        Args:
            bitrix_id: Identifier of the template;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getfields,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        select: Optional[Iterable[Text]] = MISSING,
        order: Optional[JSONDict] = MISSING,
        filter: Optional[JSONDict] = MISSING,
        start: Optional[int] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get list of templates

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/templates/document-generator-template-list.html

        The method returns a list of templates based on the filter.

        Args:
            select: An array of fields to return;

            order: Object format:
                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field used for sorting;

                - value_n is a string equal to 'asc' (ascending) or 'desc' (descending);

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }, where possible keys correspond to fields of the template;

            start: Offset pointer for pagination;

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if order is not MISSING:
            params["order"] = order

        if filter is not MISSING:
            params["filter"] = filter

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: Union[int, Text],
        *,
        fields: Optional[JSONDict] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update template

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/templates/document-generator-template-update.html

        The method updates an existing template.

        Args:
            bitrix_id: Identifier of the template;

            fields: Set of template fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if fields is not MISSING:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
