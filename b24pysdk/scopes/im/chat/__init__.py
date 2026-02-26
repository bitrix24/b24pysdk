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

    @type_checker
    def add(  # noqa: C901
            self,
            users: Iterable[Union[int, Text]],
            *,
            type: Optional[Text] = None,
            title: Optional[Text] = None,
            description: Optional[Text] = None,
            color: Optional[Text] = None,
            message: Optional[Text] = None,
            avatar: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[Union[int, Text]] = None,
            owner_id: Optional[Union[int, Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if users.__class__ is not list:
            users = list(users)

        params = dict(
            USERS=users,
        )

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

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            entity_type: Text,
            entity_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            ENTITY_TYPE=entity_type,
            ENTITY_ID=entity_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mute(
            self,
            chat_id: Union[int, Text],
            mute: Union[bool, B24BoolStrict],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            MUTE=B24BoolStrict(mute).to_b24(),
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.mute,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def leave(
            self,
            chat_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.leave,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_owner(
            self,
            chat_id: Union[int, Text],
            user_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            USER_ID=user_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.set_owner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_avatar(
            self,
            chat_id: Union[int, Text],
            avatar: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            AVATAR=avatar,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.update_avatar,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_color(
            self,
            chat_id: Union[int, Text],
            color: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            COLOR=color,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.update_color,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_title(
            self,
            chat_id: Union[int, Text],
            title: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            TITLE=title,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.update_title,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)
