from typing import Iterable, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            chat_id: int,
            users: Iterable[int],
            *,
            hide_history: Optional[Union[bool, B24BoolStrict]] = None,
            bot_id: Optional[int] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if users.__class__ is not list:
            users = list(users)

        params = {
            "CHAT_ID": chat_id,
            "USERS": users,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if hide_history is not None:
            params["HIDE_HISTORY"] = B24BoolStrict(hide_history).to_b24()

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            chat_id: int,
            user_id: int,
            *,
            bot_id: Optional[int] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
            "USER_ID": user_id,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            chat_id: int,
            *,
            bot_id: Optional[int] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
