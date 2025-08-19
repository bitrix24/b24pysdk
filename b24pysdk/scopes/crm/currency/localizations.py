from typing import TYPE_CHECKING, List, Text

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .currency import Currency


class Localizations(BaseCRM):
    """The methods offer capabilities for working with currency localization.

    Documenation: https://apidocs.bitrix24.com/api-reference/crm/currency/localizations/index.html
    """

    def __init__(self, currency: "Currency"):
        super().__init__(currency._scope)
        self._path = self._get_path(currency)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get currency localization fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/localizations/crm-currency-localizations-fields.html

        The method retrieves the available fields for currency localization, which are settings dependent on the language.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get currency localization.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/localizations/crm-currency-localizations-get.html

        This method retrieves existing currency localization.

        Args:
            bitrix_id: Currency symbolic identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            bitrix_id: Text,
            *,
            localizations: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set localization for currency.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/localizations/crm-currency-localizations-set.html

        This method updates localizations for a currency or adds them if the localization for the specified language does not exist.

        Args:
            bitrix_id: Currency identifier;

            localizations: Currency localization parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "localizations": localizations,
        }

        return self._make_bitrix_api_request(
            api_method=self.set,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: Text,
            *,
            lids: List[Text],
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete currency localization.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/localizations/crm-currency-localizations-delete.html

        This method removes currency localizations for the specified languages.

        Args:
            bitrix_id: Currency identifier;

            lids: Array of language identifiers for which localizations need to be removed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "lids": lids,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
