from functools import cached_property
from typing import Optional, Text, Union

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity
from .message import Message

__all__ = [
    "Session",
]


class Session(BaseEntity):
    """Class for managing open channels sessions.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chat-bots/index.html
    """

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @type_checker
    def finish(
            self,
            chat_id: Union[int, Text],
            *,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Finish dialog

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chat-bots/imopenlines-bot-session-finish.html

        The method ends current dialog of the open line on behalf of the application's chabot.

        Args:
            chat_id: Chat identifier;

            client_id: The parameter is required only for webhooks;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.finish,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def operator(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Switch dialog to free operator

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chat-bots/imopenlines-bot-session-operator.html

        The method switches the dialog from the chatbot to a free operator in open line.

        Args:
            chat_id: Chat identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.operator,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def transfer(
            self,
            chat_id: Union[int, Text],
            *,
            leave: Optional[bool] = MISSING,
            user_id: Optional[Union[int, Text]] = MISSING,
            queue_id: Optional[Union[int, Text]] = MISSING,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Transfer a dialogue to an operator or queue

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/chat-bots/imopenlines-bot-session-transfer.html

        The method transfers a dialogue from the chat bot in an open line to a specified operator or queue.

        Args:
            chat_id: Chat identifier;

            leave: Flag indicating the presence of the chat bot in the dialogue after the transfer;

            user_id: The identifier of the employee to whom the dialogue should be transferred;

            queue_id: The identifier of the queue to which the dialogue should be transferred;

            client_id: The parameter is required only for webhooks;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        if user_id is MISSING and queue_id is MISSING:
            raise ValueError("Either user_id or queue_id must be provided.")

        if user_id is not MISSING and queue_id is not MISSING:
            raise ValueError("Provide only one of user_id or queue_id.")

        params = dict(
            CHAT_ID=chat_id,
        )

        if leave is not MISSING:
            params["LEAVE"] = leave

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if queue_id is not MISSING:
            params["QUEUE_ID"] = queue_id

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.transfer,
            params=params,
            timeout=timeout,
        )
