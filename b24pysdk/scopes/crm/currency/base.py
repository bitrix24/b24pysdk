from typing import TYPE_CHECKING, Text

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .currency import Currency


class Base(BaseCRM):
    """The methods offer capabilities for managing base currency in which the company conducts transactions.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/index.html
    """

    def __init__(self, currency: "Currency"):
        super().__init__(currency._scope)
        self._path = self._get_path(currency)

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Get the symbolic identifier of the base currency.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/crm-currency-base-get.html

        The method retrieves the symbolic identifier of the base currency.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.get),
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            bitrix_id: Text,
            *,
            timeout: Timeout = None
    ) -> BitrixAPIRequest:
        """Set currency as base.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/crm-currency-base-set.html

        The method changes the base currency.

        Args:
            bitrix_id: Identifier of the currency that will become the base;

            timeout:Timeout in seconds.

        Returns:
            BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.set),
            params=params,
            timeout=timeout,
        )
