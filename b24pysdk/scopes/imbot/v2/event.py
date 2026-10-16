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
    """Class for retrieving bot events.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/events/index.html
    """

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
        """Get events

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/imbot.v2/events/event-get.html

        The method retrieves events for the bot in polling agent mode.

        Args:
            bot_id: Bot ID;

            bot_token: Unique authorization token for the bot;

            offset: Confirms all events with IDs less than the specified value;

            limit: Maximum number of events returned;

            with_user_events: Include user events in the response along with bot events;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
