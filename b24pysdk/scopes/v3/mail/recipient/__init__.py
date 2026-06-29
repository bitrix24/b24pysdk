from functools import cached_property
from typing import Optional, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .field import Field

__all__ = [
    "Recipient",
]


class Recipient(BaseEntity):
    """"""

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def listcontacts(
            self,
            *,
            query: Optional[Text] = None,
            pagination: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {}

        if query is not None:
            params["query"] = query

        if pagination is not None:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.listcontacts,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def listemployees(
            self,
            query: Text,
            *,
            pagination: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "query": query,
        }

        if pagination is not None:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.listemployees,
            params=params,
            timeout=timeout,
        )
