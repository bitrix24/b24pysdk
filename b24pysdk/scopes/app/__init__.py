from functools import cached_property

from ...api.requests import BitrixAPIValueRequest
from ...schemas.app import AppInfo, AppInfoApplication, AppInfoData, AppInfoWebhook
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._base_scope import BaseScope
from .option import Option

__all__ = [
    "App",
]


class App(BaseScope):
    """"""

    @cached_property
    def option(self) -> Option:
        """"""
        return Option(self)

    @type_checker
    def info(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[AppInfoData, AppInfo]:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.info,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=lambda result: AppInfoApplication.from_bitrix(result) if "ID" in result else AppInfoWebhook.from_bitrix(result),
        )
