from functools import cached_property
from typing import Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .head import Head
from .history import History
from .mode import Mode

__all__ = [
    "Session",
]


class Session(BaseEntity):
    """Class for managing operator sessions in chats.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @cached_property
    def head(self) -> Head:
        """"""
        return Head(self)

    @cached_property
    def history(self) -> History:
        """"""
        return History(self)

    @cached_property
    def mode(self) -> Mode:
        """"""
        return Mode(self)

    @type_checker
    def intercept(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Take over the dialogue from the current operator

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-intercept.html

        The method transfers the current dialogue to the operator who calls the method.

        Args:
            chat_id: Identifier of the open line chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CHAT_ID": chat_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.intercept,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def join(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Join the dialogue

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-join.html

        The method adds the current operator to an active dialogue in the open channels.

        Args:
            chat_id: Identifier of the open line chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.join,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def open(
            self,
            user_code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get chat by user code

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-open.html

        The method returns the chat ID of the line based on the user code.

        Args:
            user_code: String code of the user for the external system channel;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            USER_CODE=user_code,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.open,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def start(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Start a new dialogue

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-start.html

        The method initiates a new session in the current open line chat.

        Args:
            chat_id: Identifier of the open line chat;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.start,
            params=params,
            timeout=timeout,
        )
