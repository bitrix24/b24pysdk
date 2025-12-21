from typing import Optional, Text

from ..._base_entity import BaseEntity
from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout, JSONDict


class Pay(BaseEntity):

    @type_checker
    def payment(
            self,
            payment_id: int,
            paysystem_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Pay for an order through a specific payment system.

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-pay-payment.html

        Args:
            payment_id: Payment identifier;

            paysystem_id: Payment system identifier.

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "PAYMENT_ID": payment_id,
            "PAY_SYSTEM_ID": paysystem_id
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.payment,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def invoice(
            self,
            invoice_id: int,
            *,
            paysystem_id: Optional[int] = None,
            bx_rest_handler: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Pay for an order through a specific payment system.

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-pay-payment.html

        Args:
            invoice_id: Identifier of the old version invoice. To retrieve information about invoices, use the service crm.invoice.*;

            paysystem_id: Payment system identifier.

            bx_rest_handler: Symbolic identifier of the payment system's REST handler.

            You must pass either the PAY_SYSTEM_ID parameter or the BX_REST_HANDLER:
            when passing PAY_SYSTEM_ID, the payment system with the specified identifier is used
            when passing BX_REST_HANDLER, the first found payment system with the specified handler is used
            If both parameters are passed, the PAY_SYSTEM_ID parameter takes precedence.

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        if not paysystem_id and not bx_rest_handler:
            raise ValueError("Either PAY_SYSTEM_ID or BX_REST_HANDLER must be specified.")

        params = {
            "INVOICE_ID": invoice_id,
        }

        if paysystem_id is not None:
            params["PAY_SYSTEM_ID"] = paysystem_id

        if bx_rest_handler is not None:
            params["BX_REST_HANDLER"] = bx_rest_handler

        return self._make_bitrix_api_request(
            api_wrapper=self.invoice,
            params=params,
            timeout=timeout,
        )
