from typing import Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Networkrange",
]


class Networkrange(BaseEntity):
    """Class for managing office networks.

    Documentation: https://apidocs.bitrix24.com/api-reference/timeman/networkrange/index.html
    """

    @type_checker
    def check(
            self,
            *,
            ip: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check IP address

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/networkrange/timeman-networkrange-check.html

        The method checks whether an IP address falls within the ranges of the office network.

        Args:
            ip: The IP address to check;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if ip is not MISSING:
            params["IP"] = ip

        return self._make_bitrix_api_request(
            api_wrapper=self.check,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get network address ranges

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/networkrange/timeman-networkrange-get.html

        The method retrieves the ranges of network addresses for the office network.

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
            ranges: Iterable[JSONDict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set network address ranges

        Documentation: https://apidocs.bitrix24.com/api-reference/timeman/networkrange/timeman-networkrange-set.html

        The method sets the network address ranges for the office network.

        Args:
            ranges: Network address ranges in the form of a list of objects;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if ranges.__class__ is not list:
            ranges = list(ranges)

        params: JSONDict = {
            "ranges": ranges,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
