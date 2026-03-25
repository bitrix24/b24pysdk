from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Service",
]


class Service(BaseEntity):
    """Handle operations related to Bitrix24 catalog product services.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/service/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Add a service to the catalog.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/service/catalog-product-service-add.html

        This method adds a service to the trade catalog.

        Args:
            fields: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
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
        """
        Delete a service by identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/service/catalog-product-service-delete.html

        This method deletes a service.

        Args:
            bitrix_id: Service identifier;

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
        Download a file of a service by provided parameters.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/service/catalog-product-service-download.html

        This method downloads service files based on the provided parameters.

        Args:
            fields: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_n": "value_n",
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
        Retrieve a service by identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/service/catalog-product-service-get.html

        The method returns the field values of the service by its identifier.

        Args:
            bitrix_id: Service identifier;

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
        Retrieve service field descriptions by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/service/catalog-product-service-get-fields-by-filter.html

        The method returns service fields based on the filter.

        Args:
            filter: Object format:
                {
                    "iblockId": Identifier of the information block;
                };

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
        List services by filter.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/service/catalog-product-service-list.html

        The method returns a list of services based on the filter.

        Args:
            select: Iterable of field identifiers to select (see catalog_product_service fields). Required fields: id, iblockId;

            filter: Object format:
                {
                    "field_1": "value_1",

                    ...,

                    "field_N": "value_N",
                }
                where keys correspond to catalog_product_service fields;

            order: Object for sorting results;

            start: Start value for the API request;

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
        Update fields of a service.

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/product/service/catalog-product-service-update.html

        This method updates the service fields.

        Args:
            bitrix_id: Service identifier (catalog_product_service.id);

            fields: Object format:
                {
                    "field_1": value_1;

                    ...,

                    "field_n": value_n;
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
