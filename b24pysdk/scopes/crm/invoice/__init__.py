from functools import cached_property
from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..item.base_item import BaseItem
from .recurring import Recurring
from .status import Status
from .userfield import Userfield

__all__ = [
    "Invoice",
]


class Invoice(BaseItem):
    """"""

    @cached_property
    def recurring(self) -> Recurring:
        """"""
        return Recurring(self)

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)

    @cached_property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._add(fields, timeout=timeout)

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._delete(bitrix_id, timeout=timeout)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._fields(timeout=timeout)

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._get(bitrix_id, timeout=timeout)

    @type_checker
    def getexternallink(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getexternallink,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            select: Optional[Iterable[Text]] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._list(
            select=select,
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._update(bitrix_id, fields, timeout=timeout)
