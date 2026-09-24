from typing import Iterable

from ....._constants import MISSING
from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Link",
]


class Link(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            filter: Iterable,
            *,
            select: Iterable = MISSING,
            pagination: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if filter.__class__ is not list:
            filter = list(filter)

        params: JSONDict = {
            "filter": filter,
        }

        if select is not MISSING:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if pagination is not MISSING:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
