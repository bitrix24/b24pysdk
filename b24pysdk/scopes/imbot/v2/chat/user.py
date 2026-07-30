from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "User"

    @type_checker
    def add(
            self,
            bot_id: int,
            dialog_id: Text,
            user_ids: Iterable[int],
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_ids.__class__ is not list:
            user_ids = list(user_ids)

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "userIds": user_ids,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bot_id: int,
            dialog_id: Text,
            user_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "userId": user_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            bot_id: int,
            dialog_id: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            order: Optional[JSONDict] = MISSING,
            limit: Optional[int] = MISSING,
            offset: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        if order is not MISSING:
            params["order"] = order

        if limit is not MISSING:
            params["limit"] = limit

        if offset is not MISSING:
            params["offset"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
