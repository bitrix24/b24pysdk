from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Handler",
]


class Handler(BaseEntity):
    """Class for working with cash register handlers.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/index.html
    """

    @type_checker
    def add(
        self,
        code: Text,
        name: Text,
        settings: JSONDict,
        *,
        sort: Optional[int] = MISSING,
        supports_ffd105: Optional[bool] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add cashbox handler

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-handler-add.html

        The method adds a REST cashbox handler.

        Args:
            code: Code of the REST handler;

            name: Name of the REST handler;

            settings: Handler settings;

            sort: Sorting parameter;

            supports_ffd105: Indicates whether the cashbox supports fiscal data format version 1.05;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "CODE": code,
            "NAME": name,
            "SETTINGS": settings,
        }

        if sort is not MISSING:
            params["SORT"] = sort

        if supports_ffd105 is not MISSING:
            params["SUPPORTS_FFD105"] = bool_to_bitrix(supports_ffd105, is_required=True)

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
        """Delete cashbox handler

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-handler-delete.html

        The method deletes the REST cashbox handler.

        Args:
            bitrix_id: Identifier of the cashbox handler;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
        self,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of available cash register handlers

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-handler-list.html

        The method retrieves a list of available REST cash register handlers.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
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
        """Update cash register handler

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/cashbox/sale-cashbox-handler-update.html

        The method updates the data of the REST cash register handler.

        Args:
            bitrix_id: Identifier of the handler being updated;

            fields: Values of the fields to be updated;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": bitrix_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
