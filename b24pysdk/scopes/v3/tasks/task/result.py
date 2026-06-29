from typing import Iterable, Optional, Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, JSONList, Timeout
from ...._base_entity import BaseEntity

__all__ = [
    "Result",
]


class Result(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def addfromchatmessage(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.addfromchatmessage,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            filter: Iterable[Iterable],
            *,
            order: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            pagination: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """"""

        if filter.__class__ is not list:
            filter = list(filter)

        params = {
            "filter": filter,
        }

        if order is not None:
            params["order"] = order

        if select is not None:
            if select.__class__ is not list:
                select = list(select)

            params["select"] = select

        if pagination is not None:
            params["pagination"] = pagination

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
