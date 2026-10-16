from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Bot",
]


class Bot(BaseEntity):
    """Class for retrieving list of registered chatbots.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/outdated/bots/index.html
    """

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Deprecated"""
        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )
