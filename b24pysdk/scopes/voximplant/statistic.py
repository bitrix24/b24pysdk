from typing import Optional, Text

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
            filter: Optional[JSONDict] = None,
            sort: Optional[Text] = None,
            order: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if filter is not None:
            params["FILTER"] = filter

        if sort is not None:
            params["SORT"] = sort

        if order is not None:
            params["ORDER"] = order

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )
