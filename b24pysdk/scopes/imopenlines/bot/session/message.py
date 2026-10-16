from typing import Text, Union

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """Class for sending automatic message to the dialogue.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chat-bots/index.html
    """

    @type_checker
    def send(
            self,
            chat_id: Union[int, Text],
            message: Text,
            name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send an automatic message in the dialogue

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chat-bots/imopenlines-bot-session-message-send.html

        The method sends an automatic message from the application chatbot to the open line dialog.

        Args:
            chat_id: The identifier of the chat to which the method sends the message;

            message: The message text;

            name: The code for the auto-response type;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
            MESSAGE=message,
            NAME=name,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
