from typing import TYPE_CHECKING, Optional

from .....bitrix_api.classes import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...base_crm import BaseCRM

if TYPE_CHECKING:
    from .payment import Payment


class Product(BaseCRM):
    """These methods offer capabilities for managing product items in payments.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/products-in-payment/index.html
    """

    def __init__(self, payment: "Payment"):
        super().__init__(payment._scope)
        self._path = self._get_path(payment)

    @type_checker
    def add(
            self,
            *,
            payment_id: int,
            row_id: int,
            quantity: float,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Add product item to payment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/products-in-payment/crm-item-payment-product-add.html

        This method adds a product item to the payment.

        Args:
            payment_id: Payment identifier;

            row_id: Identifier of the product item in the CRM object;

            quantity: Quantity of the product;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "paymentId": payment_id,
            "rowId": row_id,
            "quantity": quantity,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.add),
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
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Get list of payment product items.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/products-in-payment/crm-item-payment-product-list.html

        This method retrieves a list of product items (goods or services) associated with a specific payment.

        Args:
            payment_id: Identifier of the payment;

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

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.list),
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
        """Remove product item from payment.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/products-in-payment/crm-item-payment-product-delete.html

        This method removes a product item from the payment.

        Args:
            bitrix_id: Identifier of the product item in the payment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._delete(bitrix_id, timeout=timeout)

    @type_checker
    def set_quantity(
            self,
            bitrix_id: int,
            *,
            quantity: float,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Change product quantity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/products-in-payment/crm-item-payment-product-set-quantity.html

        This method changes the quantity of a product in the payment line item.

        Args:
            bitrix_id: Identifier of the product line item in the payment;

            quantity: Quantity of the product;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "quantity": quantity,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.set_quantity),
            params=params,
            timeout=timeout,
        )
