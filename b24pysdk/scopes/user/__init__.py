from functools import cached_property
from typing import Dict, Iterable, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
from ...objects.user import User as UserObject
from ...utils.functional import type_checker
from ...utils.types import JSONDict, JSONList, Timeout
from .._adapters import BitrixObjectAdapter, BitrixObjectsAdapter
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
    ) -> BitrixAPIRequest[Dict[Text, Text]]:
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
    ) -> BitrixAPIValueRequest[int, UserObject]:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=fields,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter(UserObject, client=self._client),
        )

    @type_checker
    def get(
            self,
            *,
            sort: Optional[Text] = MISSING,
            order: Optional[Text] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            admin_mode: Optional[bool] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, UserObject]:
        """"""

        params: JSONDict = {}

        if sort is not MISSING:
            params["sort"] = sort

        if order is not MISSING:
            params["order"] = order

        if filter is not MISSING:
            params["filter"] = filter

        if admin_mode is not MISSING:
            params["ADMIN_MODE"] = int(admin_mode)

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter(UserObject, client=self._client),
        )

    @type_checker
    def update(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
            filter: Optional[JSONDict] = MISSING,
            sort: Optional[Text] = MISSING,
            order: Optional[Text] = MISSING,
            admin_mode: Optional[bool] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, UserObject]:
        """"""

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

        if sort is not MISSING:
            params["sort"] = sort

        if order is not MISSING:
            params["order"] = order

        if admin_mode is not MISSING:
            params["ADMIN_MODE"] = int(admin_mode)

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.search,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter(UserObject, client=self._client),
        )

    @type_checker
    def current(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[JSONDict, UserObject]:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.current,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter(UserObject, client=self._client),
        )

    @type_checker
    def admin(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
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
    ) -> BitrixAPIRequest[bool]:
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
