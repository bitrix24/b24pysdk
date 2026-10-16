from functools import cached_property
from typing import Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from ..._field import Field

__all__ = [
    "File",
]


class File(BaseEntity):
    """Class managing files in knowledge base.

    Documentation: https://apidocs.bitrix24.com/api-reference/note/file/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def add(
            self,
            document_id: int,
            file_name: Text,
            file_content: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Upload a file to document

        Documentation: https://apidocs.bitrix24.com/api-reference/note/file/note-file-add.html

        The method uploads a file to a document and returns a file object.

        Args:
            document_id: Identifier of the document to which the file should be attached;

            file_name: File name with extension;

            file_content: Binary file content in Base64 encoding;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "documentId": document_id,
            "fileName": file_name,
            "fileContent": file_content,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            document_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get document file data

        Documentation: https://apidocs.bitrix24.com/api-reference/note/file/note-file-get.html

        The method returns file metadata and ready-to-use Markdown block to insert the attachment into a document.

        Args:
            bitrix_id: File identifier;

            document_id: Document identifier to which the file is attached;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "documentId": document_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
