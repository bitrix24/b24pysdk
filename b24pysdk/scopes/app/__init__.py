from functools import cached_property

from ...api.requests import BitrixAPIValueRequest
from ...schemas.app import AppInfo, AppInfoApplication, AppInfoData, AppInfoWebhook
from ...utils.functional import type_checker
from ...utils.types import Timeout
from .._adapters import BitrixResultAdapter
from .._base_scope import BaseScope
from .option import Option

__all__ = [
    "App",
]


class App(BaseScope):
    """Class with system method for retrieving application information.

    Documentation: https://apidocs.bitrix24.com/api-reference/common/system/index.html
    """

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
        """Show information about the app

        Documentation: https://apidocs.bitrix24.com/api-reference/common/system/app-info.html

        The method returns information about the application.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.info,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixResultAdapter(
                lambda result: AppInfoApplication.from_bitrix(result) if "ID" in result else AppInfoWebhook.from_bitrix(result),
            ),
        )
