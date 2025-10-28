from typing import Optional, Text

from ..bitrix_api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Placement",
]


class Placement(BaseScope):
    """"""

    @type_checker
    def bind(
            self,
            placement: Text,
            handler: Text,
            *,
            title: Optional[Text] = None,
            description: Optional[Text] = None,
            group_name: Optional[Text] = None,
            lang_all: Optional[JSONDict] = None,
            options: Optional[JSONDict] = None,
            user_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "PLACEMENT": placement,
            "HANDLER": handler,
        }

        if title is not None:
            params["TITLE"] = title

        if description is not None:
            params["DESCRIPTION"] = description

        if group_name is not None:
            params["GROUP_NAME"] = group_name

        if lang_all is not None:
            params["LANG_ALL"] = lang_all

        if options is not None:
            params["OPTIONS"] = options

        if user_id is not None:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.bind,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            scope: Optional[Text] = None,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if scope is not None:
            params["SCOPE"] = scope

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unbind(
            self,
            placement: Text,
            handler: Optional[Text] = None,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "PLACEMENT": placement,
        }

        if handler is not None:
            params["HANDLER"] = handler

        return self._make_bitrix_api_request(
            api_wrapper=self.unbind,
            params=params,
            timeout=timeout,
        )
