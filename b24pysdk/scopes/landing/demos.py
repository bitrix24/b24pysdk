from typing import Annotated, Literal, Optional, Text

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
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params = dict()

        if params is not None:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def get_site_list(
            self,
            type: Annotated[Text, Literal["page", "store"]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "type": type,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_site_list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_page_list(
            self,
            type: Annotated[Text, Literal["page", "store"]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "type": type,
        }

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
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "data": data,
        }

        if params is not None:
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
