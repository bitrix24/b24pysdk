from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            chat_id: int,
            *,
            bot_id: Optional[int] = MISSING,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
        }

        if bot_id is not MISSING:
            params["BOT_ID"] = bot_id

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
