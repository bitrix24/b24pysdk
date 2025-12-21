from b24pysdk.scopes._base_entity import BaseEntity

from .....bitrix_api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout, JSONDict


class Payment(BaseEntity):

    @type_checker
    def get(
            self,
            payment_id: int,
            paysystem_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Get payment system settings for specific payment

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-settings-payment-get.html

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
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
