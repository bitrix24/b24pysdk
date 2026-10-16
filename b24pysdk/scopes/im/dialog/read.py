from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Read",
]


class Read(BaseEntity):
    """Class for marks messages as 'read'.

    Documentation: https://apidocs.bitrix24.com/api-reference/chats/index.html
    """

    @type_checker
    def __call__(
            self,
            dialog_id: Text,
            message_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[Union[JSONDict, bool]]:
        """Set the 'read' flag for messages

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/messages/im-dialog-read.html

        The method sets the 'read' flag for dialog messages up to and including the specified message.

        Args:
            dialog_id: Identifier of the chat;

            message_id: identifier of the last read message;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            DIALOG_ID=dialog_id,
            MESSAGE_ID=message_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def all(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Set the 'read' flag for all chats

        Documentation: https://apidocs.bitrix24.com/api-reference/chats/special-operations/im-dialog-read-all.html

        The method sets the 'read' flag for all chats of the current user.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.all,
            timeout=timeout,
        )
