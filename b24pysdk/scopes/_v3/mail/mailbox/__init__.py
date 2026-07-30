from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .field import Field

__all__ = [
    "Mailbox",
]


class Mailbox(BaseEntity):
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
            select: Optional[Iterable[Text]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            name: Optional[Text] = MISSING,
            email: Optional[Text] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if name is not MISSING:
            params["name"] = name

        if email is not MISSING:
            params["email"] = email

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def senders(
            self,
            pagination: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "pagination": pagination,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.senders,
            params=params,
            timeout=timeout,
        )
