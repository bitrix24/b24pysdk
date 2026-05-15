from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Section",
]


class Section(BaseEntity):
    """Handle sections in trade catalog

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/section/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add section in the catalog

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/section/catalog-section-add.html

        The method adds a section to the catalog.

        Args:
            fields: Field values for creating a new catalog section;

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
        """Delete catalog section

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/section/catalog-section-delete.html

        The method removes a section from the catalog.

        Args:
            bitrix_id: Identifier of the catalog section;

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
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields value

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/section/catalog-section-get.html

        The method returns the field values of the trade catalog section by its identifier.

        Args:
            bitrix_id: Identifier of the catalog section;

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
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields of the catalog section

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/section/catalog-section-get-fields.html

        The method returns the available fields of the catalog section.

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
        """Get a list of sections

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/section/catalog-section-list.html

        The method returns a list of sections in the trade catalog

        Args:
            select: An array with the list of fields to select;

             filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where possible values for field correspond to the fields of the catalog section;

            order: Object format:
                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the field name to sort by;

                - value_n is 'asc' for ascending or 'desc' for descending;

            start: Starting position for pagination;

            timeout: Timeout in seconds.

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

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update the catalog section

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/section/catalog-section-update.html

        The method modifies a section of the catalog.

        Args:
            bitrix_id: Identifier of the catalog section;

            fields: Field values for updating a new catalog section;

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
