from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .field import Field
from .member import Member

__all__ = [
    "Node",
]


class Node(BaseEntity):
    """"""

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @cached_property
    def member(self) -> Member:
        """"""
        return Member(self)

    @type_checker
    def add(  # noqa: C901, PLR0912
            self,
            type: Text,
            name: Text,
            parent_id: int,
            *,
            description: Optional[Text] = MISSING,
            color_name: Optional[Text] = MISSING,
            user_ids: Optional[JSONDict] = MISSING,
            move_users_to_node: Optional[bool] = MISSING,
            create_chat: Optional[bool] = MISSING,
            binding_chat_ids: Optional[Iterable[int]] = MISSING,
            create_channel: Optional[bool] = MISSING,
            binding_channel_ids: Optional[Iterable[int]] = MISSING,
            create_collab: Optional[bool] = MISSING,
            binding_collab_ids: Optional[Iterable[int]] = MISSING,
            settings: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "name": name,
            "parentId": parent_id,
        }

        if description is not MISSING:
            params["description"] = description

        if color_name is not MISSING:
            params["colorName"] = color_name

        if user_ids is not MISSING:
            params["userIds"] = user_ids

        if move_users_to_node is not MISSING:
            params["moveUsersToNode"] = move_users_to_node

        if create_chat is not MISSING:
            params["createChat"] = create_chat

        if binding_chat_ids is not MISSING:
            if binding_chat_ids.__class__ is not list:
                binding_chat_ids = list(binding_chat_ids)

            params["bindingChatIds"] = binding_chat_ids

        if create_channel is not MISSING:
            params["createChannel"] = create_channel

        if binding_channel_ids is not MISSING:
            if binding_channel_ids.__class__ is not list:
                binding_channel_ids = list(binding_channel_ids)

            params["bindingChannelIds"] = binding_channel_ids

        if create_collab is not MISSING:
            params["createCollab"] = create_collab

        if binding_collab_ids is not MISSING:
            if binding_collab_ids.__class__ is not list:
                binding_collab_ids = list(binding_collab_ids)

            params["bindingCollabIds"] = binding_collab_ids

        if settings is not MISSING:
            params["settings"] = settings

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def children(
            self,
            bitrix_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.children,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def count(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.count,
            timeout=timeout,
        )

    @type_checker
    def edit(
            self,
            bitrix_id: int,
            *,
            name: Optional[Text] = MISSING,
            description: Optional[Text] = MISSING,
            color_name: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if name is not MISSING:
            params["name"] = name

        if description is not MISSING:
            params["description"] = description

        if color_name is not MISSING:
            params["colorName"] = color_name

        return self._make_bitrix_api_request(
            api_wrapper=self.edit,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            type: Text,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def move(
            self,
            bitrix_id: int,
            parent_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "parentId": parent_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.move,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def search(
            self,
            type: Text,
            name: Text,
            *,
            parent_id: Optional[int] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "name": name,
        }

        if parent_id is not MISSING:
            params["parentId"] = parent_id

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params,
            timeout=timeout,
        )
