from typing import Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
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
            chat_id: Optional[Union[int, Text]] = None,
            dialog_id: Optional[Text] = None,
            session_id: Optional[Union[int, Text]] = None,
            user_code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if chat_id is not None:
            params["CHAT_ID"] = chat_id

        if dialog_id is not None:
            params["DIALOG_ID"] = dialog_id

        if session_id is not None:
            params["SESSION_ID"] = session_id

        if user_code is not None:
            params["USER_CODE"] = user_code

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
