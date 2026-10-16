from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "History",
]


class History(BaseEntity):
    """Class for retrieving message history and session data.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @type_checker
    def get(
            self,
            *,
            chat_id: Optional[Union[int, Text]] = MISSING,
            session_id: Optional[Union[int, Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get message history of the dialogue

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-session-history-get.html

        The method returns the message history of an open line session.

        Args:
            chat_id: Identifier of the open line chat;

            session_id: Identifier of the open line session;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if chat_id is MISSING and session_id is MISSING:
            raise ValueError("Either 'chat_id' or 'session_id' must be provided.")

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if session_id is not MISSING:
            params["SESSION_ID"] = session_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
