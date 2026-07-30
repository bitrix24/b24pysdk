from typing import Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """The messaging methods allow you to send and modify messages, work with dialogue history, context menus, and service actions in chats.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/index.html
    """

    @type_checker
    def add(
            self,
            dialog_id: Text,
            *,
            message: Optional[Text] = MISSING,
            reply_id: Optional[int] = MISSING,
            system: Optional[Union[bool, B24BoolStrict]] = MISSING,
            attach: Optional[Union[JSONDict, Text]] = MISSING,
            url_preview: Optional[Union[bool, B24BoolStrict]] = MISSING,
            keyboard: Optional[Union[JSONDict, Text]] = MISSING,
            menu: Optional[Union[JSONDict, Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[int]:
        """Send message

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-message-add.html

        The method sends a message to a chat.

        Args:
            dialog_id: Identifier of the chat in the format:

                - chatXXX — chat

                - sgXXX — group or project chat

                - XXX — identifier of the personal chat user;

            message: The text of the message;

            reply_id: Identifier of the message to which the reply is sent;

            system: Indicator of a system message;

            attach: Attachment with the content blocks;

            url_preview: Conversion of links into rich links;

            keyboard: Buttons under the message that the user can interact with;

            menu: Additional items in the chat's context menu;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
        )

        if message is not MISSING:
            params["MESSAGE"] = message

        if reply_id is not MISSING:
            params["REPLY_ID"] = reply_id

        if system is not MISSING:
            params["SYSTEM"] = B24BoolStrict(system).to_b24()

        if attach is not MISSING:
            params["ATTACH"] = attach

        if url_preview is not MISSING:
            params["URL_PREVIEW"] = B24BoolStrict(url_preview).to_b24()

        if keyboard is not MISSING:
            params["KEYBOARD"] = keyboard

        if menu is not MISSING:
            params["MENU"] = menu

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def command(
            self,
            message_id: Union[int, Text],
            bot_id: Union[int, Text],
            command: Text,
            *,
            command_params: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Execute tha chat-bot command

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-message-command.html

        The method executes a chat-bot command in the context of a message.

        Args:
            message_id: The identifier of the message in the context of which the command is executed;

            bot_id: The identifier of the bot;

            command: The bot command;

            command_params: Command parameter;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            MESSAGE_ID=message_id,
            BOT_ID=bot_id,
            COMMAND=command,
        )

        if command_params is not MISSING:
            params["COMMAND_PARAMS"] = command_params

        return self._make_bitrix_api_request(
            api_wrapper=self.command,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            message_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete message

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-message-delete.html

        The method removes message.

        Args:
            message_id: Identifier of the message;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            MESSAGE_ID=message_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def like(
            self,
            message_id: Union[int, Text],
            *,
            action: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Change status to 'Like'

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-message-like.html

        The method sets or removes the 'Like' mark for a message.

        Args:
            message_id: Identifier of the message;

            action: Action for reacting to the message;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            MESSAGE_ID=message_id,
        )

        if action is not MISSING:
            params["ACTION"] = action

        return self._make_bitrix_api_request(
            api_wrapper=self.like,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def share(
            self,
            message_id: Union[int, Text],
            dialog_id: Text,
            type: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Create an object based on the message

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-message-share.html

        The method creates an object based on a message.

        Args:
            message_id: Identifier of the message;

            dialog_id: Identifier of the chat in the format:

                - chatXXX — chat

                - sgXXX — group or project chat

                - XXX — identifier of the personal chat user;

            type: Type of the object being created;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            MESSAGE_ID=message_id,
            DIALOG_ID=dialog_id,
            TYPE=type,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.share,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            message_id: Union[int, Text],
            *,
            message: Optional[Text] = MISSING,
            attach: Optional[JSONDict] = MISSING,
            url_preview: Optional[Union[bool, B24BoolStrict]] = MISSING,
            keyboard: Optional[JSONDict] = MISSING,
            menu: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update message

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-message-update.html

        The method modifies the text and parameters of an already sent message.

        Args:
            message_id: Identifier of the message;

            message: New text of the message;

            attach: Attachment with content blocks;

            url_preview: Conversion of links into rich links;

            keyboard: Buttons below the message that the user can interact with;

            menu: Additional items in the chat's context menu;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            MESSAGE_ID=message_id,
        )

        if message is not MISSING:
            params["MESSAGE"] = message

        if attach is not MISSING:
            params["ATTACH"] = attach

        if url_preview is not MISSING:
            params["URL_PREVIEW"] = B24BoolStrict(url_preview).to_b24()

        if keyboard is not MISSING:
            params["KEYBOARD"] = keyboard

        if menu is not MISSING:
            params["MENU"] = menu

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
