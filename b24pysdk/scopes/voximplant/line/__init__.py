from functools import cached_property

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .outgoing import Outgoing

__all__ = [
    "Line",
]


class Line(BaseEntity):
    """"""

    @cached_property
    def outgoing(self) -> Outgoing:
        """Class for obtaining available outgoing lines.

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/lines/index.html
        """
        return Outgoing(self)

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of outgoing lines

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/lines/voximplant-line-get.html

        The method returns a list of available outgoing lines.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
