from typing import Text

from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "RepoWidget",
]


class RepoWidget(BaseEntity):
    """"""

    @type_checker
    def register(
            self,
            code: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "code": code,
            "fields": fields,
        }

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
    def getlist(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=api_params,
            timeout=timeout,
        )

    @type_checker
    def debug(
            self,
            enable: bool,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "enable": bool_to_bitrix(enable, is_required=True),
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.debug,
            params=params,
            timeout=timeout,
        )
