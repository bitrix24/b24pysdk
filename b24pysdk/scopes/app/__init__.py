from functools import cached_property

from ...api.requests import BitrixAPIRequest
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
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.info,
            timeout=timeout,
        )
