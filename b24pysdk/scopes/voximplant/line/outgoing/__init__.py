from functools import cached_property
from typing import Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .sip import Sip

__all__ = [
    "Outgoing",
]


class Outgoing(BaseEntity):
    """Class for managing outgoing lines.

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/lines/index.html
    """

    @cached_property
    def sip(self) -> Sip:
        """"""
        return Sip(self)

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get line for outgoing calls

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/lines/voximplant-line-outgoing-get.html

        The method returns the identifier of the current default outgoing line.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            line_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set outgoing line

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/lines/voximplant-line-outgoing-set.html

        The method sets the default outgoing line.

        Args:
            line_id: Line identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "LINE_ID": line_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
