from functools import cached_property
from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .user import User

__all__ = [
    "Chat",
]


class Chat(BaseEntity):
    """"""

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def set_owner(
            self,
            chat_id: int,
            user_id: int,
            *,
            bot_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
            "USER_ID": user_id,
        }

        if bot_id is not MISSING:
            params["BOT_ID"] = bot_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set_owner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_title(
            self,
            chat_id: int,
            title: Text,
            *,
            bot_id: Optional[int] = MISSING,
            client_id: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
            "TITLE": title,
        }

        if bot_id is not MISSING:
            params["BOT_ID"] = bot_id

        if client_id is not MISSING:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update_title,
            params=params,
            timeout=timeout,
        )
