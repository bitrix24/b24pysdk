from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Statistic",
]


class Statistic(BaseEntity):
    """"""

    @type_checker
    def get(
            self,
            *,
            filter: Optional[JSONDict] = MISSING,
            sort: Optional[Text] = MISSING,
            order: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if filter is not MISSING:
            params["FILTER"] = filter

        if sort is not MISSING:
            params["SORT"] = sort

        if order is not MISSING:
            params["ORDER"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
