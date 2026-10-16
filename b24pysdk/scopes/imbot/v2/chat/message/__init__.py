from functools import cached_property
from typing import Optional, Text

from ......_constants import MISSING
from ......api.requests import BitrixAPIRequest
from ......utils.functional import classproperty, type_checker
from ......utils.types import JSONDict, Timeout
from ....._base_entity import BaseEntity
from .reaction import Reaction

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """Class for working with messages via chatbots.

    Documentatoin: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Message"

    @cached_property
    def reaction(self) -> Reaction:
        """"""
        return Reaction(self)

    @type_checker
    def delete(
            self,
            bot_id: int,
            message_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete message

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/chat-message-delete.html

        The method deletes a message.

        Args:
            bot_id: Bot ID;

            message_id: ID of the message to be deleted;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bot_id: int,
            message_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get message

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/chat-message-get.html

        The method returns a message by its ID.

        Args:
            bot_id: Bot ID;

            message_id: ID of the message;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_context(
            self,
            bot_id: int,
            message_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            range: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get message context

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/chat-message-get-context.html

        The method returns a window of messages surrounding the specified one.

        Args:
            bot_id: Bot ID;

            message_id: ID of the message;

            bot_token: Unique authorization bot token;

            range: Number of messages on each side of the central one;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        if range is not MISSING:
            params["range"] = range

        return self._make_bitrix_api_request(
            api_wrapper=self.get_context,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def read(
            self,
            bot_id: int,
            dialog_id: Text,
            message_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Mark messages as read

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/chat-message-read.html

        The method marks messages as read on behalf of the bot.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            message_id: ID of the message;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "messageId": message_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.read,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def send(
            self,
            bot_id: int,
            dialog_id: Text,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send message

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/chat-message-send.html

        The method sends a message on behalf of the bot to the specified dialog.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            fields: Message content;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bot_id: int,
            message_id: int,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update message

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/messages/chat-message-update.html

        The method updates a bot's message.

        Args:
            bot_id: Bot ID;

            message_id: ID of the message to be updated;

            fields: Message content;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
