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
    """Class for retrieving call statistics

    Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/index.html
    """

    @type_checker
    def get(
            self,
            *,
            filter: Optional[JSONDict] = MISSING,
            sort: Optional[Text] = MISSING,
            order: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get call history list

        Documentation: https://apidocs.bitrix24.com/api-reference/telephony/voximplant/voximplant-statistic-get.html

        The method returns a list of calls from telephony statistics.

        Args:
            filter: An object for filtering;

            sort: Sorting field;

            order: Sorting direction;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
