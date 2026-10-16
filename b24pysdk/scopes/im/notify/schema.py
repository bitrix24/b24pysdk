from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Schema",
]


class Schema(BaseEntity):
    """Class for retrieving notification types schema.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/index.html
    """

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get notification type schema

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/notifications/im-notify-schema-get.html

        The method returns the schema of available notification types by modules.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
