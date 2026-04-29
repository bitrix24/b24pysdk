from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Catalog",
]


class Catalog(BaseEntity):
    """Handle operations related to Bitrix24 trading catalogs.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/catalog/index.html
    """

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve values of all fields for a specific trading catalog.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/catalog/catalog-catalog-get.html

        The method returns the values of all fields in the trade catalog.

        Args:
            bitrix_id: Identifier of the trading catalog;

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
        """Retrieve available fields of the trading catalog entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/catalog/catalog-catalog-get-fields.html

        The method returns the available fields of the trade catalog.

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
        """Retrieve a list of trading catalogs.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/catalog/catalog-catalog-list.html

        The method returns a list of trade catalogs.

        Args:
            select: Iterable of field identifiers to be selected; if omitted or empty, all fields are selected;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }, where keys correspond to catalog_catalog fields and may include prefixes such as ">= ", ">" to adjust filter behavior;

            order: Object format:
                {
                    field_1: value_1,

                    ...,
                }
                where field_n is the name of the field by which the selection will be sorted, and value_n defines the sort direction;

            start: Start position for pagination;

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
    def is_offers(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check whether the trading catalog is a variations catalog.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/catalog/catalog-catalog-is-offers.html

        The method checks if the trade catalog is a variation catalog.

        Args:
            bitrix_id: Identifier of the trading catalog;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.is_offers,
            params=params,
            timeout=timeout,
        )
