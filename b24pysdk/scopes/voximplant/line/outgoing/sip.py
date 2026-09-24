from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Sip",
]


class Sip(BaseEntity):
    """Class for managing SIP lines.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/lines/index.html
    """

    @type_checker
    def set(
            self,
            config_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set outgoing SIP line

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/lines/voximplant-line-outgoing-sip-set.html

        The method sets the SIP line as the default outgoing line.

        Args:
            config_id: Identifier of the SIP line configuration;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "CONFIG_ID": config_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
