from typing import Optional, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity


class Handler(BaseEntity):
    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        This method deletes the REST handler for the payment system

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-handler-delete.html

        Args:
             bitrix_id: Identifier of the REST handler;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
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
        """
        The method returns a list of payment systems.

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-list.html

        Args:

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            name: Text,
            code: Text,
            settings: JSONDict,
            *,
            sort: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        This method adds a REST handler for the payment system

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-handler-add.html

        Args:
             name: Name of the payment system;

             code: Code of the REST handler. Must be unique among all handlers

             settings: Handler settings. See documentation for details.

             sort: Sorting. Default is 100

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "NAME": name,
            "CODE": code,
            "SETTINGS": settings,
        }

        if sort is not None:
            params["SORT"] = sort

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
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
        """
        This method updates the REST handler for the payment system.

        Documentation: https://apidocs.bitrix24.com/api-reference/pay-system/sale-pay-system-handler-update.html

        Args:
             bitrix_id: Identifier of the REST handler;

             fields: Set of values for updating. See documentation for details.

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "ID": bitrix_id,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

