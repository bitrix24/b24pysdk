from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Paymentitemshipment",
]


class Paymentitemshipment(BaseEntity):
    """Methods for managing linking payments to shipment in the online store.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-shipment/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "paymentItemShipment"

    @type_checker
    def add(
        self,
        fields: JSONDict,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add payment binding to shipment

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-shipment/sale-payment-item-shipment-add.html

        The method adds a payment binding to a shipment.

        Args:
            fields: Field values for creating a payment binding to a shipment in the form of a structure;

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
        """Remove the binding

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-shipment/sale-payment-item-shipment-delete.html

        The method removes the payment binding to the shipment.

        Args:
            bitrix_id: Identifier of the payment binding to the shipment;

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
        """Get payment binding by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-shipment/sale-payment-item-shipment-get.html

        The method retrieves the payment binding to the shipment by ID.

        Args:
            bitrix_id: Identifier of the payment binding to the shipment;

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
    def get_fields(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-shipment/sale-payment-item-shipment-get-fields.html

        The method retrieves the available fields of the payment item shipment binding table.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
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
        """Get a list of bindings

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-shipment/sale-payment-item-shipment-list.html

        The method retrieves a list of payment bindings to shipments based on a filter.

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
        """Change payment binding to shipment

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/payment-item-shipment/sale-payment-item-shipment-update.html

        The method changes the binding of payment to shipment.

        Args:
            bitrix_id: Identifier of the payment binding to the shipment;

            fields: Field values for creating the payment binding to the shipment;

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
