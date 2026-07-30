from typing import Annotated, Literal, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Demos",
]


class Demos(BaseEntity):
    """"""

    @type_checker
    def get_list(
            self,
            *,
            params: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {}

        if params is not MISSING:
            api_params["params"] = params

        if start is not MISSING:
            api_params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def get_site_list(
            self,
            type: Annotated[Text, Literal["page", "store", "knowledge", "group", "mainpage"]],
            *,
            filter: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "type": type,
        }

        if filter is not MISSING:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.get_site_list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_page_list(
            self,
            type: Annotated[Text, Literal["page", "store", "knowledge", "group", "mainpage"]],
            *,
            filter: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "type": type,
        }

        if filter is not MISSING:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.get_page_list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def register(
            self,
            data: JSONDict,
            *,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "data": data,
        }

        if params is not MISSING:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=api_params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
