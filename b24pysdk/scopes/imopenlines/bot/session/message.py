from typing import Text, Union

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """"""

    @type_checker
    def send(
            self,
            chat_id: Union[int, Text],
            message: Text,
            name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CHAT_ID=chat_id,
            MESSAGE=message,
            NAME=name,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
