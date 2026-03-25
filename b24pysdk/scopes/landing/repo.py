from typing import Optional, Text

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
            manifest: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "code": code,
            "fields": fields,
        }

        if manifest is not None:
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
    def check_content(
            self,
            content: Text,
            *,
            splitter: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "content": content,
        }

        if splitter is not None:
            params["splitter"] = splitter

        return self._make_bitrix_api_request(
            api_wrapper=self.check_content,
            params=params,
            timeout=timeout,
        )
