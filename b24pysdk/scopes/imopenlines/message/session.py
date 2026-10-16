from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Session",
]


class Session(BaseEntity):
    """Class for starting new sessions based on the message.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/index.html
    """

    @type_checker
    def start(
            self,
            chat_id: Union[int, Text],
            message_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Start a new dialogue based on the message

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-message-session-start.html

        The method initiates a new session and transfers the specified message into it.

        Args:
            chat_id: Identifier of the open channels chat;

            message_id: Identifier of the message within the chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
            MESSAGE_ID=message_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params,
            timeout=timeout,
        )
