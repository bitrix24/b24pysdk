from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """Class for manage participants in chat groups.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "User"

    @type_checker
    def add(
            self,
            bot_id: int,
            dialog_id: Text,
            user_ids: Iterable[int],
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add participants to chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-user-add.html

        The method adds participants to the chat.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            user_ids: Array of user IDs to add;

            bot_token: Unique authorization bot token;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_ids.__class__ is not list:
            user_ids = list(user_ids)

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "userIds": user_ids,
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
            dialog_id: Text,
            user_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove a participant from the chat

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-user-delete.html

        The method removes a participant from the chat.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            user_id: User ID to be removed;

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
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            bot_id: int,
            dialog_id: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            order: Optional[JSONDict] = MISSING,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """List of chat participants

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-user-list.html

        The method returns a list of chat participants.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            bot_token: Unique authorization bot token;

            order: Parameter for sorting;

            limit: Number of records;

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

        if order is not MISSING:
            params["order"] = order

        if limit is not MISSING:
            params["limit"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
