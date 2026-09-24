from typing import Iterable, List, Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "User",
]


class User(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            chat_id: int,
            users: Iterable[int],
            *,
            hide_history: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """"""

        if users.__class__ is not list:
            users = list(users)

        params = dict(
            CHAT_ID=chat_id,
            USERS=users,
        )

        if hide_history is not MISSING:
            params["HIDE_HISTORY"] = bool_to_bitrix(hide_history, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
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
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            chat_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[List[int]]:
        """"""

        params = dict(
            CHAT_ID=chat_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
