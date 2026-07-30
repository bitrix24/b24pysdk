from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Revision",
]


class Revision(BaseEntity):
    """Method to check the compatibility of the client with the Bitrix24 server.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/im-revision-get.html"""

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get API revision

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/im-revision-get.html

        The method returns the API revision of the IM module for the current Bitrix24.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
