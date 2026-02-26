from functools import cached_property
from typing import Iterable, Optional, Text

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
    def add(  # noqa: C901
            self,
            users: Iterable[int],
            *,
            type: Optional[Text] = None,
            title: Optional[Text] = None,
            description: Optional[Text] = None,
            color: Optional[Text] = None,
            message: Optional[Text] = None,
            avatar: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            owner_id: Optional[int] = None,
            bot_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if users.__class__ is not list:
            users = list(users)

        params = dict()
        params["USERS"] = users

        if type is not None:
            params["TYPE"] = type

        if title is not None:
            params["TITLE"] = title

        if description is not None:
            params["DESCRIPTION"] = description

        if color is not None:
            params["COLOR"] = color

        if message is not None:
            params["MESSAGE"] = message

        if avatar is not None:
            params["AVATAR"] = avatar

        if entity_type is not None:
            params["ENTITY_TYPE"] = entity_type

        if entity_id is not None:
            params["ENTITY_ID"] = entity_id

        if owner_id is not None:
            params["OWNER_ID"] = owner_id

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            entity_type: Text,
            entity_id: int,
            *,
            bot_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["ENTITY_TYPE"] = entity_type
        params["ENTITY_ID"] = entity_id

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def send_typing(
            self,
            dialog_id: Text,
            *,
            bot_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["DIALOG_ID"] = dialog_id

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        return self._make_bitrix_api_request(
            api_wrapper=self.send_typing,
            params=params,
            timeout=timeout,
        )
