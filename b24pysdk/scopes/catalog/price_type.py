from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "PriceType",
]


class PriceType(BaseEntity):
    """Handle operations related to Bitrix24 catalog price types.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/
    """

    @classproperty
    def _name(cls) -> Text:
        return "priceType"

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new price type.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/catalog-price-type-add.html

        Creates a catalog price type. Only one price type can be base at any time. When a new base type is added (base = 'Y'), the previous base type loses this property.

        Args:
            fields: Object format:
                {
                    "name": "value",

                    "base": "Y|N",

                    "sort": value,

                    "xmlId": "value",
                };

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
        """Delete a price type by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/catalog-price-type-delete.html

        This method deletes a price type.

        Args:
            bitrix_id: Identifier of the price type;

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
        """Retrieve information about a price type by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/catalog-price-type-get.html

        The method returns information about the price type by its identifier.

        Args:
            bitrix_id: Identifier of the price type;

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
        """Retrieve field descriptions of the price type entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/catalog-price-type-get-fields.html

        This method returns the fields of the price type.

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
        """List price types by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/catalog-price-type-list.html

        Selects price types using the provided filter, field selection, sorting, and pagination.

        Args:
            select: Iterable of field names to select. If not provided or empty, all available fields are returned;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
                };
                where field keys correspond to catalog_price_type fields;

            order: Object format:
                {
                    "field_n": "ASC|DESC",

                    ...,
                }
                where

                - field_n is the name of the field used for sorting;

                - value is a string equal to 'ASC' (ascending) or 'DESC' (descending);

            start: Offset for pagination;

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
        """Update fields of a price type.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/price-type/catalog-price-type-update.html

        This method modifies the values of the price type fields.

        Args:
            bitrix_id: Identifier of the price type (id);

            fields: Object format:
                {
                    "name": "value",

                    "base": "Y|N",

                    "sort": value,

                    "xmlId": "value",
                };

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
