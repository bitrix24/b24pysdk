from functools import cached_property
from typing import Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import classproperty, type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .input_action import InputAction
from .manager import Manager
from .message import Message
from .text_field import TextField
from .user import User

__all__ = [
    "Chat",
]


class Chat(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Chat"

    @cached_property
    def manager(self) -> Manager:
        """"""
        return Manager(self)

    @cached_property
    def input_action(self) -> InputAction:
        """"""
        return InputAction(self)

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @cached_property
    def text_field(self) -> TextField:
        """"""
        return TextField(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def add(
            self,
            bot_id: int,
            fields: JSONDict,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "fields": fields,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bot_id: int,
            dialog_id: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def leave(
            self,
            bot_id: int,
            dialog_id: Text,
            *,
            bot_token: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
            "dialogId": dialog_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        return self._make_bitrix_api_request(
            api_wrapper=self.leave,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_owner(
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
            api_wrapper=self.set_owner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
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
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
