from typing import Optional

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Config",
]


class Config(BaseEntity):
    """Methods for real-time Push&Pull communication, including connection setup, event sending, and push notifications.

    Documentation: https://apidocs.bitrix24.com/settings/interactivity/push-and-pull/index.html
    """

    @type_checker
    def get(
            self,
            *,
            cache: Optional[bool] = MISSING,
            reopen: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get connection configuration for RT servers

        Documentation: https://apidocs.bitrix24.com/settings/interactivity/push-and-pull/pull-application-config-get.html

        The method returns the connection configuration for Push&Pull servers for the current application.

        Args:
            cache: Flag for using cached data;

            reopen: Flag for renewing channels after expiration;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if cache is not MISSING:
            params["CACHE"] = bool_to_bitrix(cache, is_required=True)

        if reopen is not MISSING:
            params["REOPEN"] = bool_to_bitrix(reopen, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
