from functools import cached_property
from typing import Optional, Text

from ......_constants import MISSING
from ......api.requests import BitrixAPIRequest
from ......utils.functional import classproperty, type_checker
from ......utils.types import JSONDict, Timeout
from ....._base_entity import BaseEntity
from .reaction import Reaction

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Message"

    @cached_property
    def reaction(self) -> Reaction:
        """"""
        return Reaction(self)

    @type_checker
    def delete(
            self,
            bot_id: int,
            message_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bot_id: int,
            message_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_context(
            self,
            bot_id: int,
            message_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            range: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        if range is not MISSING:
            params["range"] = range

        return self._make_bitrix_api_request(
            api_wrapper=self.get_context,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def read(
            self,
            bot_id: int,
            dialog_id: Text,
            message_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "messageId": message_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.read,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def send(
            self,
            bot_id: int,
            dialog_id: Text,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bot_id: int,
            message_id: int,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "messageId": message_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
