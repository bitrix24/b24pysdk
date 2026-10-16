from typing import Optional, Text

from ......_constants import MISSING
from ......api.requests import BitrixAPIRequest
from ......utils.functional import classproperty, type_checker
from ......utils.types import JSONDict, Timeout
from ....._base_entity import BaseEntity

__all__ = [
    "Reaction",
]


class Reaction(BaseEntity):
    """Class for managing reactions.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Reaction"

    @type_checker
    def add(
            self,
            bot_id: int,
            message_id: int,
            reaction: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add reaction to message

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/chat-message-reaction-add.html

        The method adds a bot reaction to a message.

        Args:
            bot_id: Bot ID;

            message_id: ID of the message to be updated;

            reaction: Reaction code;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
            "reaction": reaction,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bot_id: int,
            message_id: int,
            reaction: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete reaction from message

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/chat-message-reaction-delete.html

        The method removes the bot's reaction from a message.

        Args:
            bot_id: Bot ID;

            message_id: ID of the message to be updated;

            reaction: Reaction code;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
            "reaction": reaction,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
