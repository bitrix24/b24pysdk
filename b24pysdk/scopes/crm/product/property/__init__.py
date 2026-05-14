from functools import cached_property
from typing import Optional

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import JSONDict, Timeout
from ..._base_crm import BaseCRM
from .enumeration import Enumeration
from .settings import Settings

__all__ = [
    "Property",
]


class Property(BaseCRM):
    """"""

    @cached_property
    def enumeration(self) -> Enumeration:
        """"""
        return Enumeration(self)

    @cached_property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

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
    def list(
            self,
            *,
            filter: Optional[JSONDict] = None,
            order: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._list(
            filter=filter,
            order=order,
            start=start,
            timeout=timeout,
        )

    @type_checker
    def types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.types,
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
