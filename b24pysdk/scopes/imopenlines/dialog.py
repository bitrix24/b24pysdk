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
    """"""

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
        """"""

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
