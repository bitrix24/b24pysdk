from functools import cached_property

from .......api.requests import BitrixAPIRequest
from .......utils.functional import type_checker
from .......utils.types import JSONDict, Timeout
from ......_base_entity import BaseEntity
from .field import Field

__all__ = [
    "Message",
]


class Message(BaseEntity):
    """"""

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def send(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.send,
            params=params,
            timeout=timeout,
        )
