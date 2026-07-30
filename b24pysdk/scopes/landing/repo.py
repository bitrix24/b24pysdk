from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Repo",
]


class Repo(BaseEntity):
    """"""

    @type_checker
    def register(
            self,
            code: Text,
            fields: JSONDict,
            *,
            manifest: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "code": code,
            "fields": fields,
        }

        if manifest is not MISSING:
            params["manifest"] = manifest

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
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
    def check_content(
            self,
            content: Text,
            *,
            splitter: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "content": content,
        }

        if splitter is not MISSING:
            params["splitter"] = splitter

        return self._make_bitrix_api_request(
            api_wrapper=self.check_content,
            params=params,
            timeout=timeout,
        )
