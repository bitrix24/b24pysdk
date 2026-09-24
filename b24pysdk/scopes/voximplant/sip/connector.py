from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Connector",
]


class Connector(BaseEntity):
    """Class for obtaining status of the SIP connector.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/sip/index.html
    """

    @type_checker
    def status(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the status of the SIP connector

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/sip/voximplant-sip-connector-status.html

        The method returns the current status of the SIP connector.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.status,
            timeout=timeout,
        )
