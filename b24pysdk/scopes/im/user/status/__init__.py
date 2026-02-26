from functools import cached_property
from typing import Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ...._base_entity import BaseEntity
from .idle import Idle

__all__ = [
    "Status",
]


class Status(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @cached_property
    def idle(self) -> Idle:
        """"""
        return Idle(self)

    @type_checker
    def set(
            self,
            status: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            STATUS=status,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.set,
            params=params,
            timeout=timeout,
        )
