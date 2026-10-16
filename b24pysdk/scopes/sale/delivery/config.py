from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, JSONList, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Config",
]


class Config(BaseEntity):
    """Class for managing delivery service settings.

    Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/delivery/index.html
    """

    @type_checker
    def update(
        self,
        bitrix_id: int,
        config: JSONList,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update delivery service settings

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/delivery/sale-delivery-config-update.html

        The method updates the delivery service settings.

        Args:
            bitrix_id: Identifier of the delivery service;

            config: Values of the delivery service settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "ID": bitrix_id,
            "CONFIG": config,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
        self,
        bitrix_id: int,
        *,
        timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get delivery service settings

        Documentation: https://apidocs.bitrix24.com/api-reference/sale/delivery/delivery/sale-delivery-config-get.html

        The method retrieves the settings of the delivery service.

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
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
