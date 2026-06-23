from typing import Iterable, Optional, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Member",
]


class Member(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            node_id: int,
            user_ids: Iterable[int],
            role: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_ids.__class__ is not list:
            user_ids = list(user_ids)

        params = {
            "nodeId": node_id,
            "userIds": user_ids,
            "role": role,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def move(
            self,
            node_id: int,
            user_ids: Iterable[int],
            *,
            role: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_ids.__class__ is not list:
            user_ids = list(user_ids)

        params = {
            "nodeId": node_id,
            "userIds": user_ids,
        }

        if role is not None:
            params["role"] = role

        return self._make_bitrix_api_request(
            api_wrapper=self.move,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def remove(
            self,
            node_id: int,
            user_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_ids.__class__ is not list:
            user_ids = list(user_ids)

        params = {
            "nodeId": node_id,
            "userIds": user_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.remove,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set(
            self,
            node_id: int,
            user_ids: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "nodeId": node_id,
            "userIds": user_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
