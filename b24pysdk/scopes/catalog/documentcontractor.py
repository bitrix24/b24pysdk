from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Documentcontractor",
]


class Documentcontractor(BaseEntity):
    """Handle operations related to Bitrix24 catalog document contractor bindings.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/documentcontractor/index.html
   """

    @classproperty
    def _name(cls) -> Text:
        return "documentcontractor"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a binding of a contractor (contact or company) to an inventory management document.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/documentcontractor/catalog-documentcontractor-add.html

        This method creates a link between a CRM contractor and a store document of type "Receipt" (Приход) A.

        Args:
            fields: Object format:
                {
                    "documentId": <catalog_document.id>,

                    "entityTypeId": <integer>,

                    "entityId": <integer>,
                }, where
                - documentId — Identifier of the inventory management document of type "Receipt" A; obtainable via catalog.document.list;
                - entityTypeId — CRM object type: 3 — contact; 4 — company;
                - entityId — Identifier of the CRM element (contact or company) from the "Supplier" category;

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest."""

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
        """Delete a contractor binding from an inventory management document.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/documentcontractor/catalog-documentcontractor-delete.html

        Removes the specified contractor binding by its identifier.

        Args:
            bitrix_id: Identifier of the contractor binding;

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest."""

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
        """Retrieve a description of fields for contractor bindings.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/documentcontractor/catalog-documentcontractor-get-fields.html

        Returns field metadata for linking a contractor (contact or company) to an inventory management document.

        Args:
            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest."""
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
        """List contractor bindings for inventory management documents.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/documentcontractor/catalog-documentcontractor-list.html

        Returns a list of contractor bindings with respect to the current user's permissions. Supports pagination and sorting.

        Args:
            select: Array of catalog_documentcontractor fields to select. If omitted or empty, all available fields are returned;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }, where possible keys correspond to fields of the catalog_documentcontractor object;

            order: Object format:
                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field used for sorting;

                - value_n is a string equal to 'ASC' (ascending) or 'DESC' (descending);

            start: Offset pointer for pagination;

            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = dict()

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
            params=params,
            timeout=timeout,
        )
