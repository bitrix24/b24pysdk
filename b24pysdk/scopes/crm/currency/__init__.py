from functools import cached_property
from typing import Optional, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM
from .base import Base
from .localizations import Localizations

__all__ = [
    "Currency",
]


class Currency(BaseCRM):
    """The methods provide capabilities for managing currencies.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/index.html
    """

    @cached_property
    def base(self) -> Base:
        """"""
        return Base(self)

    @cached_property
    def localizations(self) -> Localizations:
        """"""
        return Localizations(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get currency fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/crm-currency-fields.html

        The method retrieves the description of currency fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add currency

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/crm-currency-add.html

        The method adds a new currency.

        Args:
            fields: Object format:

                {
                    CURRENCY: 'value',

                    BASE: 'value',

                    AMOUNT_CNT: 'value',

                    AMOUNT: 'value'

                    SORT: 'value'

                    LANG: 'value'
                };

            timeout: timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._add(fields=fields, timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get currency by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/crm-currency-get.html

        The method retrieves currency data by its symbolic identifier according to ISO 4217.

        Args:
            bitrix_id: Symbolic identifier of the currency;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            order: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of currencies.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/crm-currency-list.html

        The method retrieves the list of currencies created in the account.

        Args:
            order: Object format:

                {
                    field_1: order_1,

                    ...,
                }

                where

                - field_n is the name of the field by which the selection will be sorted,

                - value_n is a string value equals to 'asc' (ascending sort) or 'desc' (descending sort);

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(order=order, timeout=timeout)

    @type_checker
    def update(
            self,
            bitrix_id: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update currency.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/crm-currency-update.html

        This method updates an existing currency.

        Args:
            bitrix_id: Symbolic identifier;

            fields: Object format:

                {
                    CURRENCY: 'value',

                    BASE: 'value',

                    AMOUNT_CNT: 'value',

                    AMOUNT: 'value'

                    SORT: 'value'

                    LANG: 'value'
                };

            timeout: timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "ID": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete currency.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/currency/crm-currency-delete.html

        The method deletes a currency.

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
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
