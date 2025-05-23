from typing import Iterable, Optional, Text

from ..._bitrix_api_request import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict

from .base_crm import BaseCRM


class Orderentity(BaseCRM):
    """These methods offer capabilities for managing online store orders.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/order-entity/index.html
    """

    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Add order binding to CRM object.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/order-entity/crm-order-entity-add.html

        This method adds a binding of an order to a CRM object.

        Args:
            fields: Object format:
                {
                    "orderID": Order identifier,

                    "ownerTypeId":  Identifier of the CRM object type,

                    "ownerId": Identifier of the CRM object
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields, timeout=timeout)

    def list(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get a list of order bindings to CRM objects.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/order-entity/crm-order-entity-list.html

        This method returns a list of order bindings to CRM entities.

        Args:
            select: An array of fields to select;

            filter: Object format:

                {
                    "field_1": "value_1",

                    "field_2": "value_2",

                    ...,

                    "field_n": "value_n",
                };

            order: Object format:

                {
                    field_1: value_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            start: This parameter is used for pagination control;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self.list(
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def delete_by_filter(
            self,
            fields: JSONDict,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Remove order bindings to CRM object.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/order-entity/crm-order-entity-delete-by-filter.html

        This method removes the binding of an order to a CRM object.

        Args:
            fields: Object format:
                {
                    "orderID": Order identifier,

                    "ownerTypeId":  Identifier of the CRM object type,

                    "ownerId": Identifier of the CRM object
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params = {
            "fields": fields,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.delete_by_filter),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get order binding fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/order-entity/crm-order-entity-get-fields.html

        This method returns a list of available order binding fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.get_fields),
            timeout=timeout,
        )
