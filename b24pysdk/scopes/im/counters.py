from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Counters",
]


class Counters(BaseEntity):
    """Class for retrieving unread message counters.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/im-counters-get.html"""

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get counters

        Documentation; https://apidocs.bitrix24.com/api-reference/chats/im-counters-get.html

        The method retrieves the counters for unread messages and notifications for the current user.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
