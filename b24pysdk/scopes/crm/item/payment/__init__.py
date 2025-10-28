from functools import cached_property
from typing import Optional

from .....bitrix_api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict
from ..._base_crm import BaseCRM
from .delivery import Delivery
from .product import Product

__all__ = [
    "Payment",
]


class Payment(BaseCRM):
    """The methods provide capabilities for managing payments.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/index.html
    """

    @cached_property
    def delivery(self) -> Delivery:
        """"""
        return Delivery(self)

    @cached_property
    def product(self) -> Product:
        """"""
        return Product(self)

    @type_checker
    def add(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Add payment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/crm-item-payment-add.html

        This method creates a payment for a CRM object.

        Args:
            entity_type_id: Identifier of the CRM object type;

            entity_id: Identifier of the CRM object;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get payment by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/crm-item-payment-get.html

        This method retrieves brief information about the payment.

        Args:
            bitrix_id: Payment identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            entity_type_id: int,
            entity_id: int,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get a list of payments.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/crm-item-payment-list.html

        Args:
            entity_type_id: Identifier of the CRM entity type;

            entity_id: Identifier of the CRM entity;

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

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "entityTypeId": entity_type_id,
            "entityId": entity_id,
        }

        if filter is not None:
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Update payment fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/crm-item-payment-update.html

        This method updates a limited set of payment fields.

        Args:
            bitrix_id: Payment identifier;

            fields: Object format:
                {
                    "paid": payment status, where "Y" for paid and "N" is not paid,

                    "paySystemId":  Payment system identifier
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._update(bitrix_id, fields, timeout=timeout)

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Delete payment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/crm-item-payment-delete.html

        This method deletes a payment.

        Args:
            bitrix_id: Payment identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)

    @type_checker
    def pay(
            self,
            bitrix_id: int,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Change payment status to "Paid".

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/crm-item-payment-pay.html

        This method changes the payment status to "Paid".

        Args:
            bitrix_id: Payment identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.pay,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpay(
            self,
            bitrix_id: int,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Change payment status to "Unpaid".

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/crm-item-payment-unpay.html

        This method changes the payment status to "Unpaid".

        Args:
            bitrix_id: Payment identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unpay,
            params=params,
            timeout=timeout,
        )
