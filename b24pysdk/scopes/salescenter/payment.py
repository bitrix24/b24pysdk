from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Payment",
]


class Payment(BaseEntity):
    """Class for obtaining payment link in CRM objects.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/index.html
    """

    @type_checker
    def get_public_url(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Generate a link for a specific payment

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/universal/payment/salescenter-payment-get-public-url.html

        This method generates a link for a specific payment.
        The payment method selected will be passed to this particular payment.

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
            api_wrapper=self.get_public_url,
            params=params,
            timeout=timeout,
        )
