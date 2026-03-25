from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Element",
]


class Element(BaseEntity):
    """
    Handle operations related to Bitrix24 inventory document items (document elements).

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/document-element/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Create a document element (product position) in an inventory document.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/document-element/catalog-document-element-add.html

        Adds a product line to the specified stock management document.

        Args:
            fields: Object format:
                {
                    "field_n": value_n,

                    "field_n": value_n,

                    ...
                };

                where
                    - field_n — field of the element for creating;
                    - value_n — field value;

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
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Delete a document element from an inventory document by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/document-element/catalog-document-element-delete.html

        Args:
            bitrix_id: Identifier of the product record in the document.

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
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the list of available fields for document elements.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/document-element/catalog-document-element-get-fields.html

        The API returns field descriptions.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
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
        """
        List document elements with selection, filtering, sorting, and pagination options.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/document-element/catalog-document-element-list.html

        Returns product positions associated with inventory documents. Records are limited by document types available to the user and warehouse access rights.

        Args:
            select: Iterable of catalog_document_element field names to select.

            filter: Object format:
                {
                    "field_n": value_n,

                    "field_n": value_n,

                    ...
                }

                where
                    - field_n — field of the element for filtering;
                    - value_n — field value;

            order: Object format:
                {
                    field_n: value_n,
                    ...,
                }
                where
                - field_n is the name of the field to sort by;
                - value_n is a string 'ASC' (ascending) or 'DESC' (descending);

            start: Pagination start position for batch listing.

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """


        params: JSONDict = {}

        if select is not None:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
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
        """
        Update an existing document element and return the updated data.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/document/document-element/catalog-document-element-update.html

        Args:
            bitrix_id: Identifier of the document item to update.

            fields: Object format:
                {
                    "field_n": value_n,

                    "field_n": value_n,

                    ...
                };

                where
                    - field_n — field of the element for updating;
                    - value_n — field value;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
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
