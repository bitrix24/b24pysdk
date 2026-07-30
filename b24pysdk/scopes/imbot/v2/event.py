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
            bot_id: int,
            *,
            bot_token: Optional[Text] = MISSING,
            offset: Optional[int] = MISSING,
            limit: Optional[int] = MISSING,
            with_user_events: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "botId": bot_id,
        }

        if bot_token is not MISSING:
            params["botToken"] = bot_token

        if offset is not MISSING:
            params["offset"] = offset

        if limit is not MISSING:
            params["limit"] = limit

        if with_user_events is not MISSING:
            params["withUserEvents"] = with_user_events

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
