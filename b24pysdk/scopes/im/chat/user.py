from typing import Iterable, List, Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for managing participants in chats.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-users/index.html
    """

    @type_checker
    def add(
            self,
            chat_id: int,
            users: Iterable[int],
            *,
            hide_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Invite participants to chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-users/im-chat-user-add.html

        The method adds users to a chat.

        Args:
            chat_id: Chat ID;

            users: Array of user identifiers to be added to the chat;

            hide_history: Hide chat history for added users;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if users.__class__ is not list:
            users = list(users)

        params = dict(
            CHAT_ID=chat_id,
            USERS=users,
        )

        if hide_history is not MISSING:
            params["HIDE_HISTORY"] = bool_to_bitrix(hide_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            chat_id: int,
            user_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Exclude participants from chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-users/im-chat-user-delete.html

        The method removes a user from the chat.

        Args:
            chat_id: Chat ID;

            user_id: User identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
            USER_ID=user_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            chat_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[int]]:
        """Get chat participants IDs

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/chat-users/im-chat-user-list.html

        The method returns a list of chat participant IDs.

        Args:
            chat_id: Chat ID;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
