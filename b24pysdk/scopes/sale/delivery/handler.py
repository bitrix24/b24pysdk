from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Handler",
]


class Handler(BaseEntity):
    """Class for working with delivery service handlers in online stores.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/handler/index.html
    """

    @type_checker
    def add(
        self,
        code: Text,
        name: Text,
        settings: JSONDict,
        profiles: JSONList,
        *,
        sort: Optional[int] = MISSING,
        description: Optional[Text] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add delivery service handler

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/handler/sale-delivery-handler-add.html

        The method adds a delivery service handler.

        Args:
            code: Symbolic code of the delivery service handler;

            name: Name of the delivery service handler;

            settings: Object containing information about the settings of the delivery service handler;

            profiles: Array containing a list of delivery profiles objects;

            sort: Sorting;

            description: Description of the delivery service handler;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "CODE": code,
            "NAME": name,
            "SETTINGS": settings,
            "PROFILES": profiles,
        }

        if sort is not MISSING:
            params["SORT"] = sort

        if description is not MISSING:
            params["DESCRIPTION"] = description

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
        self,
        bitrix_id: int,
        *,
        code: Optional[Text] = MISSING,
        name: Optional[Text] = MISSING,
        sort: Optional[int] = MISSING,
        description: Optional[Text] = MISSING,
        settings: Optional[JSONDict] = MISSING,
        profiles: Optional[JSONList] = MISSING,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update delivery service handler

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/handler/sale-delivery-handler-update.html

        The method updates the delivery service handler.

        Args:
            bitrix_id: Identifier of the delivery service handler;

            code: Symbolic code of the delivery service handler;

            name: Name of the delivery service handler;

            sort: Sorting;

            description: Description of the delivery service handler;

            settings: Object containing information about the settings of the delivery service handler;

            profiles: Array containing a list of delivery profiles objects;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": bitrix_id,
        }

        if code is not MISSING:
            params["CODE"] = code

        if name is not MISSING:
            params["NAME"] = name

        if sort is not MISSING:
            params["SORT"] = sort

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if settings is not MISSING:
            params["SETTINGS"] = settings

        if profiles is not MISSING:
            params["PROFILES"] = profiles

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
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
        """Delete delivery service handler

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/handler/sale-delivery-handler-delete.html

        The method deletes the delivery service handler.

        Args:
            bitrix_id: Identifier of the delivery service;

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
        """Get a list of delivery service handlers

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/handler/sale-delivery-handler-list.html

        The method retrieves a list of delivery service handlers.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )
