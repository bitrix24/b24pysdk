from functools import cached_property
from typing import Iterable, Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .user import User

__all__ = [
    "Chat",
]


class Chat(BaseEntity):
    """Class for managing chats.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/index.html
    """

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def add(  # noqa: C901
            self,
            *,
            users: Iterable[Union[int, Text]] = MISSING,
            type: Optional[Text] = MISSING,
            title: Optional[Text] = MISSING,
            description: Optional[Text] = MISSING,
            color: Optional[Text] = MISSING,
            message: Optional[Text] = MISSING,
            avatar: Text = MISSING,
            entity_type: Optional[Text] = MISSING,
            entity_id: Optional[Union[int, Text]] = MISSING,
            copilot_main_role: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[int]:
        """Create chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/im-chat-add.html

        The method creates a new chat.

        Args:
            users: An array of users IDs to be added to the chat;

            type: Type of the chat;

            title: Title of the chat;

            description: Description of the chat;

            color: Color of the chat;

            message: The first message in the chat;

            avatar: The avatar of the chat in base64 format;

            entity_type: Type of object to link the chat with external context;

            entity_id: Identifier of the object within entity_type;

            copilot_main_role: Code of the main role for BitrixGPT;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params: JSONDict = {}

        if users is not MISSING:
            if users.__class__ is not list:
                users = list(users)

            params["USERS"] = users

        if type is not MISSING:
            params["TYPE"] = type

        if title is not MISSING:
            params["TITLE"] = title

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if color is not MISSING:
            params["COLOR"] = color

        if message is not MISSING:
            params["MESSAGE"] = message

        if avatar is not MISSING:
            params["AVATAR"] = avatar

        if entity_type is not MISSING:
            params["ENTITY_TYPE"] = entity_type

        if entity_id is not MISSING:
            params["ENTITY_ID"] = entity_id

        if copilot_main_role is not MISSING:
            params["COPILOT_MAIN_ROLE"] = copilot_main_role

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            entity_type: Text,
            entity_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Optional[JSONDict]]:
        """Get chat ID

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/im-chat-get.html

        The method retrieves the chat ID.

        Args:
            entity_type: Type of object to link the chat with external context;

            entity_id: Identifier of the object within entity_type;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            ENTITY_TYPE=entity_type,
            ENTITY_ID=entity_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mute(
            self,
            *,
            chat_id: int = MISSING,
            dialog_id: Text = MISSING,
            mute: bool = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/special-operations/im-chat-mute.html

        The method disables or enables notifications in the specified chat.

        Args:
            chat_id: Identifier of the chat if dialog_id is not provided;

            dialog_id: The chat identifier;

            mute: Notification control;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if dialog_id is not MISSING:
            params["DIALOG_ID"] = dialog_id

        if mute is not MISSING:
            params["MUTE"] = mute
        params: JSONDict = {}

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if dialog_id is not MISSING:
            params["DIALOG_ID"] = dialog_id

        if mute is not MISSING:
            params["MUTE"] = bool_to_bitrix(mute, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.mute,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def leave(
            self,
            chat_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Leave chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-users/im-chat-leave.html

        The method removes the current user from the chat.

        Args:
            chat_id: Identifier of the chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.leave,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_owner(
            self,
            user_id: Union[int, Text],
            *,
            chat_id: int = MISSING,
            dialog_id: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Change chat owner

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-update/im-chat-set-owner.html

        The method changes the owner of the chat.

        Args:
            user_id: Identifier of the new chat owner;

            chat_id: Identifier of the chat if dialog_id is not provided;

            dialog_id: The chat identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {"USER_ID": user_id}

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if dialog_id is not MISSING:
            params["DIALOG_ID"] = dialog_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set_owner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_avatar(
            self,
            avatar: Text,
            *,
            chat_id: int = MISSING,
            dialog_id: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update chat avatar

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-update/im-chat-update-avatar.html

        The method updates the chat avatar.

        Args:
            avatar: Identifier of the new chat owner;

            chat_id: Identifier of the chat if dialog_id is not provided;

            dialog_id: The chat identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {"AVATAR": avatar}

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if dialog_id is not MISSING:
            params["DIALOG_ID"] = dialog_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update_avatar,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_color(
            self,
            color: Text,
            *,
            chat_id: int = MISSING,
            dialog_id: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update chat color

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-update/im-chat-update-color.html

        The method updates the chat color.

        Args:
            color: Identifier of the new chat owner;

            chat_id: Identifier of the chat if dialog_id is not provided;

            dialog_id: The chat identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {"COLOR": color}

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if dialog_id is not MISSING:
            params["DIALOG_ID"] = dialog_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update_color,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_title(
            self,
            title: Text,
            *,
            chat_id: int = MISSING,
            dialog_id: Text = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Update chat title

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-update/im-chat-update-title.html

        The method updates the chat color.

        Args:
            title: Identifier of the new chat owner;

            chat_id: Identifier of the chat if dialog_id is not provided;

            dialog_id: The chat identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest"""

        params: JSONDict = {"TITLE": title}

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if dialog_id is not MISSING:
            params["DIALOG_ID"] = dialog_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update_title,
            params=params,
            timeout=timeout,
        )
