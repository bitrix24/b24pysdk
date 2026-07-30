from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Get",
]


class Get(BaseEntity):
    """"""

    @type_checker
    def __call__(
            self,
            type: Text,
            owner_id: int,
            *,
            from_date: Optional[Text] = MISSING,
            to: Optional[Text] = MISSING,
            section: Optional[Iterable[int]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "ownerId": owner_id,
        }

        if from_date is not MISSING:
            params["from"] = from_date

        if to is not MISSING:
            params["to"] = to

        if section is not MISSING:
            if section.__class__ is not list:
                section = list(section)

            params["section"] = section

        return self._make_bitrix_api_request(
            api_wrapper=self,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def nearest(
            self,
            *,
            type: Optional[Text] = MISSING,
            owner_id: Optional[int] = MISSING,
            days: Optional[int] = MISSING,
            for_current_user: Optional[bool] = MISSING,
            max_events_count: Optional[int] = MISSING,
            detail_url: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if type is not MISSING:
            params["type"] = type

        if owner_id is not MISSING:
            params["ownerId"] = owner_id

        if days is not MISSING:
            params["days"] = days

        if for_current_user is not MISSING:
            params["forCurrentUser"] = for_current_user

        if max_events_count is not MISSING:
            params["maxEventsCount"] = max_events_count

        if detail_url is not MISSING:
            params["detailUrl"] = detail_url

        return self._make_bitrix_api_request(
            api_wrapper=self.nearest,
            params=params,
            timeout=timeout,
        )
