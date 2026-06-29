from typing import Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
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
            filter_controller: Optional[Text] = None,
            filter_method: Optional[Text] = None,
            filter_module: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if filter_controller is not None:
            params["filterController"] = filter_controller

        if filter_method is not None:
            params["filterMethod"] = filter_method

        if filter_module is not None:
            params["filterModule"] = filter_module

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
