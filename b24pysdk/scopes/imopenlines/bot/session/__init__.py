from functools import cached_property
from typing import Optional, Text, Union

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import B24BoolStrict, Timeout
from ...._base_entity import BaseEntity
from .message import Message

__all__ = [
    "Session",
]


class Session(BaseEntity):
    """"""

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

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)

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
            leave: Union[bool, B24BoolStrict],
            *,
            user_id: Optional[Union[int, Text]] = None,
            queue_id: Optional[Union[int, Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if user_id is None and queue_id is None:
            raise ValueError("Either user_id or queue_id must be provided.")

        if user_id is not None and queue_id is not None:
            raise ValueError("Provide only one of user_id or queue_id.")

        params = dict(
            CHAT_ID=chat_id,
            LEAVE=B24BoolStrict(leave).to_b24(),
        )

        if user_id is not None:
            params["USER_ID"] = user_id

        if queue_id is not None:
            params["QUEUE_ID"] = queue_id

        return self._make_bitrix_api_request(
            api_wrapper=self.transfer,
            params=params,
            timeout=timeout,
        )
