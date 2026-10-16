from functools import cached_property
from typing import Text, Union

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity
from .idle import Idle

__all__ = [
    "Status",
]


class Status(BaseEntity):
    """Class for managing user's chat status.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/index.html
    """

    @cached_property
    def idle(self) -> Idle:
        """"""
        return Idle(self)

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Union[Text, bool]]:
        """Get user status

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/im-user-status-get.html

        The method returns the status of the current user.

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
            status: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Set user status

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/users/im-user-status-set.html

        The method sets current user's status.

        Args:
            status: The new status of the user;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            STATUS=status,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
