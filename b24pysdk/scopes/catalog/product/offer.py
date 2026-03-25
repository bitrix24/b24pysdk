from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Offer",
]


class Offer(BaseEntity):
    """
    Handle operations related to Bitrix24 product offers (variations).

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/offer/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Create a product offer (variation) in the catalog.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/offer/catalog-product-offer-add.html

        This method adds a new product offer by sending field values to the REST API.

        Args:
            fields: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
                }, values correspond to catalog_product_offer fields used for creating an offer;

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
        Delete a product offer by identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/offer/catalog-product-offer-delete.html

        This method deletes a product variation.

        Args:
            bitrix_id: Identifier of the product offer (catalog_product_offer.id);

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
    def download(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Download files of a product offer by the provided parameters.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/offer/catalog-product-offer-download.html

        This method downloads product variation files based on the provided parameters.

        Args:
            fields: Object format:
                {
                    "fileId": integer,

                    "productId": integer,

                    "fieldName": string,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.download,
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
        """
        Retrieve information about a specific product offer by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/offer/catalog-product-offer-get.html

        The method returns the field values of a product variation by its identifier.

        Args:
            bitrix_id: Identifier of the product offer;

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
    def get_fields_by_filter(
            self,
            filter: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve field descriptions of product offers by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/offer/catalog-product-offer-get-fields-by-filter.html

        This method returns the fields of a product variation based on the filter.

        Args:
            filter: Object format:
                {

                    "iblockId": integer,
                }, where iblockId is the identifier of the catalog information block for offers;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "filter": filter,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields_by_filter,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            select: Iterable[Text],
            filter: JSONDict,
            *,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Return a list of product offers by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/offer/catalog-product-offer-list.html

        The method returns a list of product variations based on the filter.

        Args:
            select: Iterable of field names to select; required fields include id and iblockId;

            filter: Object format:
                {
                    "field_1": "value_1",
                    ...,
                    "field_N": "value_N",
                }, possible keys correspond to catalog_product_offer fields;

            order: Object format:
                {
                    field_1: value_1,
                    ...,
                }
                where
                - field_n is the field name to sort by
                - value_n is either 'ASC' (ascending) or 'DESC' (descending);

            start: Starting position for selection if pagination is used;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if select.__class__ is not list:
            select = list(select)

        params: JSONDict = {
            "select": select,
            "filter": filter,
        }

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
        """
        Update fields of a product offer.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/offer/catalog-product-offer-update.html

        This method updates the fields of a product variation.

        Args:
            bitrix_id: Identifier of the product offer;

            fields: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
                }, where the keys correspond to catalog_product_offer fields;

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
