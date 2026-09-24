from functools import cached_property
from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .element import Element
from .mode import Mode

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """Class for working with inventory accounting in the trade catalog.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create inventory document

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-add.html

        The method creates a new inventory document.

        Args:
            fields: Document fields;

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
    def cancel(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Cancel document of inventory accounting

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-cancel.html

        The method cancels the conduct of the inventory accounting document.

        Args:
            bitrix_id: Identifier of the document;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.cancel,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def cancel_list(
            self,
            document_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Canceling multiple documents

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-cancel-list.html

        The method cancels the processing of a group of inventory documents.

        Args:
            document_ids: A list of document identifiers;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if document_ids.__class__ is not list:
            document_ids = list(document_ids)

        params: JSONDict = {
            "documentIds": document_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.cancel_list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def conduct(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Conduct warehouse accounting document

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-conduct.html

        The method conducts a warehouse accounting document.

        Args:
            bitrix_id: Identifier of the document;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.conduct,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def conduct_list(
            self,
            document_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Conduct multiple warehouse accounting documents

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-conduct-list.html

        The method conducts a group of warehouse accounting documents.

        Args:
            document_ids: A list of document identifiers;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if document_ids.__class__ is not list:
            document_ids = list(document_ids)

        params: JSONDict = {
            "documentIds": document_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.conduct_list,
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
        """Delete inventory document

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-delete.html

        The method removes an inventory document.

        Args:
            bitrix_id: Identifier of the document;

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
    def delete_list(
            self,
            document_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete multiple inventory documents

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-delete-list.html

        The method removes multiple inventory documents.

        Args:
            document_ids: A list of document identifiers;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if document_ids.__class__ is not list:
            document_ids = list(document_ids)

        params: JSONDict = {
            "documentIds": document_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete_list,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def element(self) -> Element:
        """"""
        return Element(self)

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of fields for inventory document

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-get-fields.html

        The method returns the description of fields for the inventory document.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of warehouse accounting documents

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-list.html

        The method returns a paginated list of warehouse accounting documents.

        Args:
            select: An array of fields that need to be selected;

            filter: An object for filtering the selected documents;

            order: An object for sorting the selected documents;

            start: This parameter is used for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def mode(self) -> Mode:
        """"""
        return Mode(self)

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update warehouse accounting document

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/catalog-document-update.html

        The method modifies the fields of an existing warehouse accounting document.

        Args:
            bitrix_id: Document identifier;

            fields: Document fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
