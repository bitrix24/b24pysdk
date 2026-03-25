from typing import Iterable, Optional, Text

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
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
            from_date: Optional[Text] = None,
            to: Optional[Text] = None,
            section: Optional[Iterable[int]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "ownerId": owner_id,
        }

        if from_date is not None:
            params["from"] = from_date

        if to is not None:
            params["to"] = to

        if section is not None:
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
            type: Optional[Text] = None,
            owner_id: Optional[int] = None,
            days: Optional[int] = None,
            for_current_user: Optional[bool] = None,
            max_events_count: Optional[int] = None,
            detail_url: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if type is not None:
            params["type"] = type

        if owner_id is not None:
            params["ownerId"] = owner_id

        if days is not None:
            params["days"] = days

        if for_current_user is not None:
            params["forCurrentUser"] = for_current_user

        if max_events_count is not None:
            params["maxEventsCount"] = max_events_count

        if detail_url is not None:
            params["detailUrl"] = detail_url

        return self._make_bitrix_api_request(
            api_wrapper=self.nearest,
            params=params,
            timeout=timeout,
        )
