from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Eventlog",
]


class Eventlog(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            select: Optional[Iterable[Text]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if select is not None:
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
            select: Optional[Iterable[Text]] = None,
            filter: Optional[Iterable] = None,
            order: Optional[JSONDict] = None,
            pagination: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if select is not None:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if filter is not None:
            if filter.__class__ is not list:
                filter = list(filter)
            params["filter"] = filter

        if order is not None:
            params["order"] = order

        if pagination is not None:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def tail(
            self,
            *,
            select: Optional[Iterable[Text]] = None,
            filter: Optional[Iterable] = None,
            cursor: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if select is not None:
            if select.__class__ is not list:
                select = list(select)
            params["select"] = select

        if filter is not None:
            if filter.__class__ is not list:
                filter = list(filter)
            params["filter"] = filter

        if cursor is not None:
            params["cursor"] = cursor

        return self._make_bitrix_api_request(
            api_wrapper=self.tail,
            params=params,
            timeout=timeout,
        )
