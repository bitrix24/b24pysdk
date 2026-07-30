from typing import Optional, Text

from ......_constants import MISSING
from ......api.requests import BitrixAPIRequest
from ......utils.functional import classproperty, type_checker
from ......utils.types import JSONDict, Timeout
from ....._base_entity import BaseEntity

__all__ = [
    "Reaction",
]


class Reaction(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Reaction"

    @type_checker
    def add(
            self,
            bot_id: int,
            message_id: int,
            reaction: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
            "reaction": reaction,
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
            message_id: int,
            reaction: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
            "reaction": reaction,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
