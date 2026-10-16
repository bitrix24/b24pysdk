from typing import Optional

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Idle",
]


class Idle(BaseEntity):
    """Class for managing user's automatic Away chat status.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/index.html
    """

    @type_checker
    def end(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Disable automatic status 'Away'

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/im-user-status-idle-end.html

        The method disables the automatic 'Away' status.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.end,
            timeout=timeout,
        )

    @type_checker
    def start(
            self,
            *,
            ago: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Enable automatic status 'Away'

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/im-user-status-idle-start.html

        The method enables the automatic status 'Away' for the current user.

        Args:
            ago: How many minutes ago to set the 'Away' status;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if ago is not MISSING:
            params["AGO"] = ago

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params or None,
            timeout=timeout,
        )
