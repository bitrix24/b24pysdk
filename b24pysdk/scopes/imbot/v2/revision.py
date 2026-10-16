from typing import Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Revision",
]


class Revision(BaseEntity):
    """Class for checking which revision is installed.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Revision"

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get API revision

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/revision-get.html

        The method returns the revision numbers of the REST API and client protocols of the messanger.

        Args:
             timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )
