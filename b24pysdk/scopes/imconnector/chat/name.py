from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Name",
]


class Name(BaseEntity):
    """Class for changing chat name.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/index.html
    """

    @type_checker
    def set(
            self,
            connector: Text,
            line: Union[int, Text],
            chat_id: Text,
            name: Text,
            *,
            user_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Set a new chat name

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/imconnector/imconnector-chat-name-set.html

        The method sets a new name for the chat.

        Args:
            connector: The string code of the connector;

            line: Identifier of the Open Channel;

            chat_id: Identifier of the chat in the external system;

            name: New name for the chat;

            user_id: User identifier;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = dict(
            CONNECTOR=connector,
            LINE=line,
            CHAT_ID=chat_id,
            NAME=name,
        )

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
