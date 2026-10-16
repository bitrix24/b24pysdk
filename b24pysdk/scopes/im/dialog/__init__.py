from functools import cached_property
from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .messages import Messages
from .read import Read
from .users import Users

__all__ = [
    "Dialog",
]


class Dialog(BaseEntity):
    """Class for working with dialogs.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/index.html
    """

    @cached_property
    def messages(self) -> Messages:
        """"""
        return Messages(self)

    @cached_property
    def read(self) -> Read:
        """"""
        return Read(self)

    @cached_property
    def users(self) -> Users:
        """"""
        return Users(self)

    @type_checker
    def get(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get chat data

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/im-dialog-get.html

        The method retrieves information about a chat.

        Args:
            dialog_id: Chat identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unread(
            self,
            dialog_id: Text,
            message_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Set the 'unread' flag for messages

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-dialog-unread.html

        The method sets the 'unread' flag for messages in a dialog starting from the specified message.

        Args:
            dialog_id: Chat identifier;

            message_id: Identifier of the first unread message;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
            MESSAGE_ID=message_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.unread,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def writing(
            self,
            dialog_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Send 'User is typing' indicator

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-dialog-writing.html

        The method sends a 'User is typing' indicator to the chat.

        Args:
            dialog_id: Chat identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.writing,
            params=params,
            timeout=timeout,
        )
