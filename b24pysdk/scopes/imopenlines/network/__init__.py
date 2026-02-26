from functools import cached_property
from typing import Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..._base_entity import BaseEntity
from .message import Message

__all__ = [
    "Network",
]


class Network(BaseEntity):
    """"""

    @type_checker
    def join(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CODE=code,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.join,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def message(self) -> Message:
        """"""
        return Message(self)
