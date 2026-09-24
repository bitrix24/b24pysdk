from functools import cached_property
from typing import Optional, Text, Union

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.converters import bool_to_bitrix
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity
from .message import Message

__all__ = [
    "Session",
]


class Session(BaseEntity):
    """"""

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

    @type_checker
    def finish(
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
            api_wrapper=self.finish,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def operator(
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
            api_wrapper=self.operator,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def transfer(
            self,
            chat_id: Union[int, Text],
            leave: bool,
            *,
            user_id: Optional[Union[int, Text]] = MISSING,
            queue_id: Optional[Union[int, Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id is MISSING and queue_id is MISSING:
            raise ValueError("Either user_id or queue_id must be provided.")

        if user_id is not MISSING and queue_id is not MISSING:
            raise ValueError("Provide only one of user_id or queue_id.")

        params = dict(
            CHAT_ID=chat_id,
            LEAVE=bool_to_bitrix(leave, is_required=True),
        )

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if queue_id is not MISSING:
            params["QUEUE_ID"] = queue_id

        return self._make_bitrix_api_request(
            api_wrapper=self.transfer,
            params=params,
            timeout=timeout,
        )
