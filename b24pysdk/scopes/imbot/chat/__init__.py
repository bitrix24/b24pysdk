from functools import cached_property
from typing import Iterable, Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
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

        params = {
            "USERS": users,
        }

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

        params = {
            "ENTITY_TYPE": entity_type,
            "ENTITY_ID": entity_id,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def leave(
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
            api_wrapper=self.leave,
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

        params = {
            "DIALOG_ID": dialog_id,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        return self._make_bitrix_api_request(
            api_wrapper=self.send_typing,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_owner(
            self,
            chat_id: int,
            user_id: int,
            *,
            bot_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
            "USER_ID": user_id,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set_owner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_manager(
            self,
            chat_id: int,
            user_id: int,
            *,
            is_manager: Optional[Union[bool, B24BoolStrict]] = None,
            bot_id: Optional[int] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
            "USER_ID": user_id,
        }

        if is_manager is not None:
            params["IS_MANAGER"] = B24BoolStrict(is_manager).to_b24()

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.set_manager,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_avatar(
            self,
            chat_id: int,
            avatar: Text,
            *,
            bot_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
            "AVATAR": avatar,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update_avatar,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_color(
            self,
            chat_id: int,
            color: Text,
            *,
            bot_id: Optional[int] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
            "COLOR": color,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update_color,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_title(
            self,
            chat_id: int,
            title: Text,
            *,
            bot_id: Optional[int] = None,
            client_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CHAT_ID": chat_id,
            "TITLE": title,
        }

        if bot_id is not None:
            params["BOT_ID"] = bot_id

        if client_id is not None:
            params["CLIENT_ID"] = client_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update_title,
            params=params,
            timeout=timeout,
        )
