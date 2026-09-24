from functools import cached_property

from .......api.requests import BitrixAPIRequest
from .......utils.functional import type_checker
from .......utils.types import JSONDict, Timeout
from ......_base_entity import BaseEntity
from ....._field import Field

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """Class for sending messages in task chats.

    Documentation: https://apidocs.bitrix24.com/api-reference/tasks/index.html
    """

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def send(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Send a message in task chat

        Documentation: https://apidocs.bitrix24.com/api-reference/tasks/tasks-task-chat-message-send.html

        The method sends a new message to the task chat.

        Args:
            fields: An object with message parameters;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
