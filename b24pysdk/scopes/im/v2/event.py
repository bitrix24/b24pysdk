from typing import Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Event",
]


class Event(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "Event"

    @type_checker
    def get(
            self,
            offset: int,
            *,
            limit: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "offset": offset,
        }

        if limit is not MISSING:
            params["limit"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def subscribe(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.subscribe,
            timeout=timeout,
        )

    @type_checker
    def unsubscribe(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.unsubscribe,
            timeout=timeout,
        )
