from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Agreement",
]


class Agreement(BaseEntity):
    """"""

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
    def text(
            self,
            *,
            bitrix_id: Optional[Text] = None,
            replace: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if bitrix_id is not None:
            params["id"] = bitrix_id

        if replace is not None:
            params["replace"] = replace

        return self._make_bitrix_api_request(
            api_wrapper=self.text,
            params=params or None,
            timeout=timeout,
        )
