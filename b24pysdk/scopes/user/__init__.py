from functools import cached_property
from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_scope import BaseScope
from .option import Option
from .userfield import Userfield

__all__ = [
    "User",
]


class User(BaseScope):
    """"""

    @cached_property
    def option(self) -> Option:
        """"""
        return Option(self)

    @cached_property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.fields,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=fields,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            sort: Optional[Text] = None,
            order: Optional[Text] = None,
            filter: Optional[JSONDict] = None,
            admin_mode: Optional[bool] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if sort is not None:
            params["sort"] = sort

        if order is not None:
            params["order"] = order

        if filter is not None:
            params["filter"] = filter

        if admin_mode is not None:
            params["ADMIN_MODE"] = int(admin_mode)

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=fields,
            timeout=timeout,
        )

    @type_checker
    def search(
            self,
            *,
            filter: Optional[JSONDict] = None,
            sort: Optional[Text] = None,
            order: Optional[Text] = None,
            admin_mode: Optional[bool] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if filter is not None:
            params["filter"] = filter

        if sort is not None:
            params["sort"] = sort

        if order is not None:
            params["order"] = order

        if admin_mode is not None:
            params["ADMIN_MODE"] = int(admin_mode)

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def current(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.current,
            timeout=timeout,
        )

    @type_checker
    def admin(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.admin,
            timeout=timeout,
        )

    @type_checker
    def access(
            self,
            access: Iterable[Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if access.__class__ is not list:
            access = list(access)

        params: JSONDict = {
            "ACCESS": access,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.access,
            params=params,
            timeout=timeout,
        )
