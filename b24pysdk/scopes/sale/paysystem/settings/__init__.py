from functools import cached_property

from .payment import Payment
from ...._base_entity import BaseEntity
from .....bitrix_api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout, JSONDict

_all__ = [
    "Settings",
]


class Settings(BaseEntity):

    @cached_property
    def payment(self) -> Payment:
        return Payment(self)

    @type_checker
    def get(
            self,
            sale_paysystem_id: int,
            *,
            person_type_id: int = 0,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Get Settings for Payment System by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-settings-get.html

        Args:
            sale_paysystem_id: Identifier of the payment system for which to retrieve settings;

            person_type_id: Identifier of the payer type for which to retrieve settings. To get default settings, pass 0.

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ID": sale_paysystem_id,
            "PERSON_TYPE_ID": person_type_id
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            sale_payment_id: int,
            person_type_id: int,
            settings: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Update payment system settings.

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-settings-update.html

        Args:
            sale_payment_id: Identifier of the payment system for which settings need to be retrieved;

            person_type_id: Identifier of the payer type for which settings need to be retrieved.

            settings: Settings to be updated.

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ID": sale_payment_id,
            "PERSON_TYPE_ID": person_type_id,
            "SETTINGS": settings
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
