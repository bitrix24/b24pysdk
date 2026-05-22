from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24Bool, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """Methods for working with documents.

    Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/index.html
    """

    @type_checker
    def add(
        self,
        template_id: int,
        *,
        value: Optional[Text] = None,
        values: Optional[JSONDict] = None,
        stamps_enabled: Optional[Union[bool, int]] = None,
        fields: Optional[JSONDict] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new document

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/document-generator-document-add.html

        The method creates a new document based on a template.

        Args:
            template_id: Template identifier;

            value: External identifier of the object for which the document is being generated;

            values: Object format:
                {
                    'field': 'value'
                } - field values of the document in the format;

            stamps_enabled: Seal and signature mode;

            fields: Description of how to interpret and format values from values;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "templateId": template_id,
        }

        if value is not None:
            params["value"] = value

        if values is not None:
            params["values"] = values

        if stamps_enabled is not None:
            params["stampsEnabled"] = B24Bool(stamps_enabled).to_b24()

        if fields is not None:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
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
        """Delete document

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/document-generator-document-delete.html

        The method removes a document by its identifier.

        Args:
            bitrix_id: Document identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
    def enablepublicurl(
        self,
        bitrix_id: int,
        status: Union[bool, int],
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Enable or disable public link for document

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/document-generator-document-enable-public-url.html

        The method enables or disables the public link for a document.

        Args:
            bitrix_id: Document identifier;

            status: Status of the public link;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
            "status": B24Bool(status).to_b24(),
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.enablepublicurl,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get document by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/document-generator-document-get.html

        The method returns information about a document by its ID.

        Args:
            bitrix_id: Document identifier;

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
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of fields for the document

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/document-generator-document-get-fields.html

        The method returns the fields of the document, along with their current and base values.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.getfields,
            timeout=timeout,
        )

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
        """Get the list of documents

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/document-generator-document-list.html

        The method returns a list of documents based on the filter.

        Args:
            select: An array containing the list of fields to return;

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
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {}

        if select is not None:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if order is not None:
            params["order"] = order

        if filter is not None:
            params["filter"] = filter

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: int,
        *,
        values: Optional[JSONDict] = None,
        stamps_enabled: Optional[Union[bool, int]] = None,
        fields: Optional[JSONDict] = None,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update existing document

        Documentation: https://apidocs.bitrix24.com/api-reference/document-generator/document-generator-document-update.html

        The method updates a document with new field values.

        Args:
            bitrix_id: Document identifier;

            values: Object format:
                {
                    'field': 'value'
                } - field values of the document in the format;

            stamps_enabled: Seal and signature mode;

            fields: Description of how to interpret and format values from values;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        if values is not None:
            params["values"] = values

        if stamps_enabled is not None:
            params["stampsEnabled"] = B24Bool(stamps_enabled).to_b24()

        if fields is not None:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
