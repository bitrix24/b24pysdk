from typing import Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Dialog",
]


class Dialog(BaseEntity):
    """Class to obtain information about dialogs.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/outdated/chats/index.html
    """

    @type_checker
    def get(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Deprecated"""

        params = {
            "DIALOG_ID": dialog_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
