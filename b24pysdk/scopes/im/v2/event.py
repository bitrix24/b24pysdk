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
    """Class for managing user messanger events.

    Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/im.v2/events/index.html
    """

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
        """Retrieve user events

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/im.v2/events/event-get.html

        The method retrieves events for the current user in polling mode.

        Args:
            offset: Confirms processed events and returns events starting from this value;

            limit: Maximum number of events returned;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Subscribe to events

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/im.v2/events/event-subscribe.html

        The method subscribes the current user to event logging.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
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
        """Unsubscribe from events

        Documentation: https://apidocs.bitrix24.com/api-reference/chat-bots/chat-bots-v2/im.v2/events/event-unsubscribe.html

        The method cancels the current user's subscription to event logging.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.unsubscribe,
            timeout=timeout,
        )
