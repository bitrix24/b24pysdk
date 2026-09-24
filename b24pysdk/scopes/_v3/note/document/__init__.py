from functools import cached_property
from typing import Optional

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from ..._field import Field
from .search import Search
from .tree import Tree

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """Class for managing documents in knowledge base.

    Documentation: https://apidocs.bitrix24.com/api-reference/note/document/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @cached_property
    def search(self) -> Search:
        """"""
        return Search(self)

    @cached_property
    def tree(self) -> Tree:
        """"""
        return Tree(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create document

        Documentation: https://apidocs.bitrix24.com/api-reference/note/document/note-document-add.html

        The method creates a new document in the knowledge base and returns its object.

        Args:
            fields: Object with the fields of the new document;

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
    def archive(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Archive a document

        Documentation: https://apidocs.bitrix24.com/api-reference/note/document/note-document-archive.html

        The method archives a document and all its child pages.

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
            api_wrapper=self.archive,
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
        """Move document to the trash

        Documentation: https://apidocs.bitrix24.com/api-reference/note/document/note-document-delete.html

        The method moves the document and its child pages to the trash.

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
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get document

        Documentation: https://apidocs.bitrix24.com/api-reference/note/document/note-document-get.html

        THe method returns a single document with its content in Markdown.

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
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            overwrite: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update document

        Documentation: https://apidocs.bitrix24.com/api-reference/note/document/note-document-update.html

        THe method updates the heading and/or the content of a document.

        Args:
            bitrix_id: Document identifier;

            fields: Object with the fields to be changed;

            overwrite: Determines whether to force overwrite the document content if it has unsaved changes from a collaborative editor;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        if overwrite is not MISSING:
            params["overwrite"] = overwrite

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
