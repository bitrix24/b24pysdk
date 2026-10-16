from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Manager",
]


class Manager(BaseEntity):
    """Class for managing chat managers.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Manager"

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
        """Add chat managers

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-manager-add.html

        The method adds users to the current list of chat managers.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            user_ids: Array of user IDs to assign as managers;

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
            user_ids: Iterable[int],
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Remove chat managers

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/chats/chat-manager-delete.html

        The method removes users from the chat managers list.

        Args:
            bot_id: Bot ID;

            dialog_id: Dialog ID;

            user_ids: Array of user IDs to remove the manager role;

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
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
