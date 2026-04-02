from functools import cached_property

from ......api.requests import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import Timeout
from ....._base_entity import BaseEntity
from .field import Field

__all__ = [
    "Access",
]


class Access(BaseEntity):
    """"""

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
