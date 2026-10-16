from functools import cached_property
from typing import Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .input_action import InputAction
from .manager import Manager
from .message import Message
from .text_field import TextField
from .user import User

__all__ = [
    "Chat",
]


class Chat(BaseEntity):
    """Class for working with group chats on behalf of a bot.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Chat"

    @cached_property
    def manager(self) -> Manager:
        """"""
        return Manager(self)

    @cached_property
    def input_action(self) -> InputAction:
        """"""
        return InputAction(self)

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @cached_property
    def text_field(self) -> TextField:
        """"""
        return TextField(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def add(
            self,
            bot_id: int,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a group chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-add.html

        The method creates a new group chat on behalf of the bot.

        Args:
            bot_id: Bot ID;

            fields: Properties of the chat being created;

            bot_token: Unique authorization bot token;

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
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bot_id: int,
            dialog_id: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-get.html

        The method returns information about the chat.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def leave(
            self,
            bot_id: int,
            dialog_id: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Leave chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-leave.html

        The method removes the bot from chat.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.leave,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_owner(
            self,
            bot_id: int,
            dialog_id: Text,
            user_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Assign chat owner

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-set-owner.html

        The method transfers chat ownership to another user.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            user_id: ID of the new chat owner;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "userId": user_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.set_owner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bot_id: int,
            dialog_id: Text,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update chat properties

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-update.html

        The method updates chat properties.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            fields: Properties of the chat to be updated;

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
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
