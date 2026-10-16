from typing import Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Dialog",
]


class Dialog(BaseEntity):
    """Class for retrieving operator dialog data.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

    @type_checker
    def get(
            self,
            *,
            chat_id: Optional[Union[int, Text]] = MISSING,
            dialog_id: Optional[Text] = MISSING,
            session_id: Optional[Union[int, Text]] = MISSING,
            user_code: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the operator's dialog

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/sessions/imopenlines-dialog-get.html

        The method returns data from the open line chat.

        Args:
            chat_id: Identifier of the open line chat;

            dialog_id: Identifier of the open line dialog;

            session_id: Identifier of the session;

            user_code: String code of the user for the external system channel;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if chat_id is not MISSING:
            params["CHAT_ID"] = chat_id

        if dialog_id is not MISSING:
            params["DIALOG_ID"] = dialog_id

        if session_id is not MISSING:
            params["SESSION_ID"] = session_id

        if user_code is not MISSING:
            params["USER_CODE"] = user_code

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
