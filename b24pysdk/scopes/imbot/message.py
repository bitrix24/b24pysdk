from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """"""

    @type_checker
    def delete(
            self,
            message_id: int,
            *,
            bot_id: Optional[int] = MISSING,
            complete: Optional[Text] = MISSING,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "MESSAGE_ID": message_id,
        }

        if bot_id is not MISSING:
            params["BOT_ID"] = bot_id

        if complete is not MISSING:
            params["COMPLETE"] = complete

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def like(
            self,
            message_id: int,
            *,
            bot_id: Optional[int] = MISSING,
            action: Optional[Text] = MISSING,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "MESSAGE_ID": message_id,
        }

        if bot_id is not MISSING:
            params["BOT_ID"] = bot_id

        if action is not MISSING:
            params["ACTION"] = action

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.like,
            params=params,
            timeout=timeout,
        )
