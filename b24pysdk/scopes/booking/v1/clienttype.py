from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Clienttype",
]


class Clienttype(BaseEntity):
    """Handle operations related to Bitrix24 booking client types.

    Documentation: https://apidocs.bitrix24.com/api-reference/booking/index.html
    """

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the list of available client types.

        Documentation: https://apidocs.bitrix24.com/api-reference/booking/booking-v1-clienttype-list.html

        The method returns a list of available client types.

        Args:
            timeout: Timeout in seconds;

        Returns:
            Instance of BitrixAPIRequest.
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )
