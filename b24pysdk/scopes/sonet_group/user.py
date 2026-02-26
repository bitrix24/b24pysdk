from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            group_id: int,
            user_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            group_id: int,
            user_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def groups(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.groups,
            timeout=timeout,
        )

    @type_checker
    def invite(
            self,
            group_id: int,
            user_id: Union[int, Iterable[int]],
            *,
            message: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        if message is not None:
            params["MESSAGE"] = message

        return self._make_bitrix_api_request(
            api_wrapper=self.invite,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def request(
            self,
            group_id: int,
            *,
            message: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "GROUP_ID": group_id,
        }

        if message is not None:
            params["MESSAGE"] = message

        return self._make_bitrix_api_request(
            api_wrapper=self.request,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            group_id: int,
            user_id: Union[int, Iterable[int]],
            role: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id.__class__ is not list and not isinstance(user_id, int):
            user_id = list(user_id)

        params = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
            "ROLE": role,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
