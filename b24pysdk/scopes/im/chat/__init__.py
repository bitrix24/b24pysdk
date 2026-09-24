from functools import cached_property
from typing import Iterable, Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
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
            users: Iterable[Union[int, Text]],
            *,
            type: Optional[Text] = MISSING,
            title: Optional[Text] = MISSING,
            description: Optional[Text] = MISSING,
            color: Optional[Text] = MISSING,
            message: Optional[Text] = MISSING,
            avatar: Text = MISSING,
            entity_type: Optional[Text] = MISSING,
            entity_id: Optional[Union[int, Text]] = MISSING,
            owner_id: Optional[Union[int, Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[int]:
        """"""

        if users.__class__ is not list:
            users = list(users)

        params = dict(
            USERS=users,
        )

        if type is not MISSING:
            params["TYPE"] = type

        if title is not MISSING:
            params["TITLE"] = title

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if color is not MISSING:
            params["COLOR"] = color

        if message is not MISSING:
            params["MESSAGE"] = message

        if avatar is not MISSING:
            params["AVATAR"] = avatar

        if entity_type is not MISSING:
            params["ENTITY_TYPE"] = entity_type

        if entity_id is not MISSING:
            params["ENTITY_ID"] = entity_id

        if owner_id is not MISSING:
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
    ) -> BitrixAPIRequest[Optional[JSONDict]]:
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
            mute: bool,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            MUTE=bool_to_bitrix(mute, is_required=True),
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.mute,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def leave(
            self,
            chat_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
            chat_id: int,
            user_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
            chat_id: int,
            avatar: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
            chat_id: int,
            color: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
            chat_id: int,
            title: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
