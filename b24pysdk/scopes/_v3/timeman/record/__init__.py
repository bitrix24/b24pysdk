from functools import cached_property
from typing import Iterable, Optional, Text

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity
from .field import Field

__all__ = [
    "Record",
]


class Record(BaseEntity):
    """"""

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @type_checker
    def list(
            self,
            filter: Iterable,
            *,
            select: Optional[Iterable[Text]] = MISSING,
            order: Optional[JSONDict] = MISSING,
            pagination: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if filter.__class__ is not list:
            filter = list(filter)

        params = {
            "filter": filter,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if order is not MISSING:
            params["order"] = order

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
