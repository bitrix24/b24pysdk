from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Paymentitembasket",
]


class Paymentitembasket(BaseEntity):
    """A set of methods for managing cart item bindings in the online store.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-basket/index.html
    """

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add basket item binding to payment

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-basket/sale-payment-item-basket-add.html

        The method adds a binding of a basket item to a payment.

        Args:
            fields: Field values for creating a binding of a basket item to a payment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
        """Delete the binding of the cart item to the payment

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-basket/sale-payment-item-basket-delete.html

        The method removes the binding of a cart item to a payment.

        Args:
            bitrix_id: Identifier of the binding of the cart item to the payment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
        """Get values of all fields for the basket item binding to payment

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-basket/sale-payment-item-basket-get.html

        The method retrieves the values of all fields for the basket item binding to payment.

        Args:
            bitrix_id: Identifier of the basket item binding to payment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
    def getfields(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get available fields for payment item basket bindings

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-basket/sale-payment-item-basket-get-fields.html

        The method retrieves the available fields for payment item basket bindings.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.getfields,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        select: Optional[Iterable[Text]] = MISSING,
        filter: Optional[JSONDict] = MISSING,
        order: Optional[JSONDict] = MISSING,
        start: Optional[int] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of basket item bindings to payments

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-basket/sale-payment-item-basket-list.html

        The method retrieves a list of bindings of basket items to payments.

        Args:
            select: An array of fields to be selected;

            filter: An object for filtering the selected records;

            order: An object for sorting the selected records, where the key is the field and the value is asc or desc;

            start: This parameter is used to manage pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
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
        """Update the binding of the cart item to the payment

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-basket/sale-payment-item-basket-update.html

        The method updates the binding of the cart item to the payment.

        Args:
            bitrix_id: Identifier of the binding of the cart item to the payment;

            fields: Field values for updating the binding of the cart item to the payment;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
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
