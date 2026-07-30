from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Scope",
]


class Scope(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            *,
            filter_controller: Optional[Text] = MISSING,
            filter_method: Optional[Text] = MISSING,
            filter_module: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if filter_controller is not MISSING:
            params["filterController"] = filter_controller

        if filter_method is not MISSING:
            params["filterMethod"] = filter_method

        if filter_module is not MISSING:
            params["filterModule"] = filter_module

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
