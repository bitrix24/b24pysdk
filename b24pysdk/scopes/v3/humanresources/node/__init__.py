from functools import cached_property
from typing import Iterable, Optional, Text

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
            description: Optional[Text] = None,
            color_name: Optional[Text] = None,
            user_ids: Optional[JSONDict] = None,
            move_users_to_node: Optional[bool] = None,
            create_chat: Optional[bool] = None,
            binding_chat_ids: Optional[Iterable[int]] = None,
            create_channel: Optional[bool] = None,
            binding_channel_ids: Optional[Iterable[int]] = None,
            create_collab: Optional[bool] = None,
            binding_collab_ids: Optional[Iterable[int]] = None,
            settings: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "name": name,
            "parentId": parent_id,
        }

        if description is not None:
            params["description"] = description

        if color_name is not None:
            params["colorName"] = color_name

        if user_ids is not None:
            params["userIds"] = user_ids

        if move_users_to_node is not None:
            params["moveUsersToNode"] = move_users_to_node

        if create_chat is not None:
            params["createChat"] = create_chat

        if binding_chat_ids is not None:
            if binding_chat_ids.__class__ is not list:
                binding_chat_ids = list(binding_chat_ids)

            params["bindingChatIds"] = binding_chat_ids

        if create_channel is not None:
            params["createChannel"] = create_channel

        if binding_channel_ids is not None:
            if binding_channel_ids.__class__ is not list:
                binding_channel_ids = list(binding_channel_ids)

            params["bindingChannelIds"] = binding_channel_ids

        if create_collab is not None:
            params["createCollab"] = create_collab

        if binding_collab_ids is not None:
            if binding_collab_ids.__class__ is not list:
                binding_collab_ids = list(binding_collab_ids)

            params["bindingCollabIds"] = binding_collab_ids

        if settings is not None:
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
            select: Optional[Iterable[Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if select is not None:
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
            name: Optional[Text] = None,
            description: Optional[Text] = None,
            color_name: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if name is not None:
            params["name"] = name

        if description is not None:
            params["description"] = description

        if color_name is not None:
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
            select: Optional[Iterable[Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if select is not None:
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
            select: Optional[Iterable[Text]] = None,
            pagination: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
        }

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if pagination is not None:
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
            parent_id: Optional[int] = None,
            pagination: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "name": name,
        }

        if parent_id is not None:
            params["parentId"] = parent_id

        if pagination is not None:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params,
            timeout=timeout,
        )
