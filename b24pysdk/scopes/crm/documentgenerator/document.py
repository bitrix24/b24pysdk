from typing import TYPE_CHECKING, Iterable, Optional, Text

from ....bitrix_api.classes.bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .documentgenerator import Documentgenerator


class Document(BaseCRM):
    """The methods provide capabilities for working with documents.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/index.html
    """

    def __init__(self, documentgenerator: "Documentgenerator"):
        super().__init__(documentgenerator._scope)
        self._path = self._get_path(documentgenerator)

    @type_checker
    def getfields(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get document fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/crm-document-generator-document-get-fields.html

        The method returns a list of document fields along with their description.

        Args:
            bitrix_id: Document identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.getfields,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            *,
            template_id: int,
            entity_type_id: int,
            entity_id: int,
            values: JSONDict,
            stamps_enabled: bool,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new document.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/crm-document-generator-document-add.html

        The method creates a new document based on a template and data from the corresponding entity.

        Args:
            template_id: Identifier of the template;

            entity_type_id: CRM entity type ID;

            entity_id: Identifier of the CRM entity;

            values: Additional field values;

            stamps_enabled: Stamps and signatures, where True - enable, False - disable;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "templateId": template_id,
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "values": values,
            "stampsEnabled": stamps_enabled,
        }

        return self._make_bitrix_api_request(
            api_method=self.add,
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
        """Get document information.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/crm-document-generator-document-get.html

        The method returns information about a document by its identifier.

        Args:
            bitrix_id: Identifier of the document;

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
        """Get the list of documents.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/crm-document-generator-document-list.html

        The method returns a list of documents based on the filter.

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
            *,
            values: JSONDict,
            stamps_enabled: bool,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update document.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/crm-document-generator-document-update.html

        The method updates an existing document with new values

        Args:
            bitrix_id: Document identifier;

            values: Array of new field values for the document;

            stamps_enabled: Stamps and signatures, where True - enable, False - disable;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "values": values,
            "stampsEnabled": stamps_enabled,
        }

        return self._make_bitrix_api_request(
            api_method=self.update,
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
        """Delete document.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/crm-document-generator-document-delete.html

        The method removes a document.

        Args:
            bitrix_id: Document identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id=bitrix_id, timeout=timeout)

    @type_checker
    def enablepublicurl(
            self,
            bitrix_id: int,
            *,
            status: bool,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Enable and disable public link for document.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/crm-document-generator-document-enable-public-url.html

        The method enables/disables thr public link for the document.

        Args:
            bitrix_id: Document identifier;

            status: Status of the public link for the document, where True - enable, False - disable;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "status": status,
        }

        return self._make_bitrix_api_request(
            api_method=self.enablepublicurl,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def upload(
            self,
            *,
            file_content: Text,
            region: Text,
            entity_type_id: int,
            entity_id: int,
            title: Text,
            number: int,
            pdf_content: Optional[Text] = None,
            image_content: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Upload and attach the generated document.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/document-generator/documents/crm-document-generator-document-upload.html

        The method uploads a generated document and attaches it to the specified entity.

        Args:
            file_content: Content of the docx file in base64;

            region: Country;

            entity_type_id: Identifier of the CRM entity type;

            entity_id: Identifier of the CRM entity;

            title: Document title;

            number: Document number;

            pdf_content: Content of the pdf file in base64;

            image_content: Content of the image in base64;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fileContent": file_content,
            "region": region,
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
            "title": title,
            "number": number,
        }

        if pdf_content is not None:
            params["pdfContent"] = pdf_content

        if image_content is not None:
            params["imageContent"] = image_content

        return self._make_bitrix_api_request(
            api_method=self.upload,
            params=params,
            timeout=timeout,
        )
