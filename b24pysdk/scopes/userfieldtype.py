from typing import Optional, Text

from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Userfieldtype",
]


class Userfieldtype(BaseScope):
    """"""

    @type_checker
    def add(
            self,
            user_type_id: Text,
            handler: Text,
            *,
            title: Optional[Text] = None,
            description: Optional[Text] = None,
            options: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "USER_TYPE_ID": user_type_id,
            "HANDLER": handler,
        }

        if title is not None:
            params["TITLE"] = title

        if description is not None:
            params["DESCRIPTION"] = description

        if options is not None:
            params["OPTIONS"] = options

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            user_type_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "USER_TYPE_ID": user_type_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            user_type_id: Text,
            handler: Text,
            title: Text,
            *,
            description: Optional[Text] = None,
            options: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "USER_TYPE_ID": user_type_id,
            "HANDLER": handler,
            "TITLE": title,
        }

        if description is not None:
            params["DESCRIPTION"] = description

        if options is not None:
            params["OPTIONS"] = options

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
