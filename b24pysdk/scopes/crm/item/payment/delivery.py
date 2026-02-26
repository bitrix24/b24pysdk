from typing import Optional

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ..._base_crm import BaseCRM

__all__ = [
    "Delivery",
]


class Delivery(BaseCRM):
    """These methods provide capabilities for managing deliveries in payments.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/delivery-in-payment/index.html
    """

    @type_checker
    def add(
            self,
            *,
            payment_id: int,
            delivery_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add delivery item to payment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/delivery-in-payment/crm-item-payment-delivery-add.html

        This method adds a delivery item to the payment.

        Args:
            payment_id: Payment identifier;

            delivery_id: Delivery identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "paymentId": payment_id,
            "deliveryId": delivery_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            payment_id: int,
            filter: JSONDict,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of delivery items.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/delivery-in-payment/crm-item-payment-delivery-list.html

        This method retrieves the list of delivery items for a specific payment.

        Args:
            payment_id: Payment identifier.

            filter: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
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
            "paymentId": payment_id,
            "filter": filter,
        }

        if order is not None:
            params["order"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
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
        """Remove delivery item from payment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/delivery-in-payment/crm-item-payment-delivery-delete.html

        This method removes a delivery item from the payment.

        Args:
            bitrix_id: Identifier of the delivery item in the payment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)

    @type_checker
    def set_delivery(
            self,
            bitrix_id: int,
            *,
            delivery_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Reassign delivery item to another document.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/delivery-in-payment/crm-item-payment-delivery-set-delivery.html

        This method reassigns a delivery item to another delivery document.

        Args:
            bitrix_id: Identifier of the delivery item in the payment;

            delivery_id: Identifier of the delivery;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "deliveryId": delivery_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set_delivery,
            params=params,
            timeout=timeout,
        )
