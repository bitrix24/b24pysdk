from typing import TYPE_CHECKING, Optional, Text

from ...bitrix_api.classes import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ..scope import Scope
from .userfield import Userfield

if TYPE_CHECKING:
    from ... import Client

__all__ = [
    "User",
]


class User(Scope):
    """"""

    def __init__(self, client: "Client"):
        super().__init__(client)
        self.userfield = Userfield(self)

    @type_checker
    def fields(
            self,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_method=self.fields,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            fields: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_method=self.add,
            params=fields,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            sort: Optional[Text] = None,
            order: Optional[Text] = None,
            filter: Optional[JSONDict] = None,
            admin_mode: Optional[bool] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

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
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            fields: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_method=self.update,
            params=fields,
            timeout=timeout,
        )

    @type_checker
    def current(
            self,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_method=self.current,
            timeout=timeout,
        )

    @type_checker
    def search(
            self,
            filter: Optional[JSONDict] = None,
            sort: Optional[Text] = None,
            order: Optional[Text] = None,
            admin_mode: Optional[bool] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

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
            api_method=self.search,
            params=params,
            timeout=timeout,
        )
