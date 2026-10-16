from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Command",
]


class Command(BaseEntity):
    """Class for managing the slash commands of the chatbot.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/commands/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Command"

    @type_checker
    def answer(
            self,
            bot_id: int,
            command_id: int,
            message_id: int,
            dialog_id: Text,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Responding to the command

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/commands/command-answer.html

        The method sends the bot's response to a slash command call.

        Args:
            bot_id: Bot ID;

            command_id: Command ID;

            message_id: Message ID with the command;

            dialog_id: Dialog ID;

            fields: Fields of the response message;

            bot_token: Unique authorization token for the bot;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "commandId": command_id,
            "messageId": message_id,
            "dialogId": dialog_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.answer,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            bot_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of commands

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/commands/command-list.html

        The method returns a list of all bot commands.

        Args:
            bot_id: Bot ID;

            bot_token: Unique authorization token for the bot;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            bot_id: int,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Register a slash command

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/commands/command-register.html

        The method register a bot slash command.

        Args:
            bot_id: Bot ID;

            fields: Object with command parameters;

            bot_token: Unique authorization token for the bot;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            bot_id: int,
            command_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove the slash command

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/commands/command-unregister.html

        The method removes the bot's slash command.

        Args:
            bot_id: Bot ID;

            command_id: Command ID;

            bot_token: Unique authorization token for the bot;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "commandId": command_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bot_id: int,
            command_id: int,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update the slash command

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/commands/command-update.html

        The method updates the bot's slash command.

        Args:
            bot_id: Bot ID;

            command_id: Command ID;

            fields: Object with command parameters;

            bot_token: Unique authorization token for the bot;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "commandId": command_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
