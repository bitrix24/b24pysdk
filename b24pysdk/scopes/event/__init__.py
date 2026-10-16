from functools import cached_property
from typing import Annotated, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
from ...constants.event import EventTypeLiteral
from ...objects.event import Event as EventObject
from ...schemas.results import CountResultData
from ...utils.functional import type_checker
from ...utils.types import JSONDict, JSONList, Timeout
from .._adapters import BitrixObjectsAdapter, BitrixResultAdapter
from .._base_scope import BaseScope
from .offline import Offline

__all__ = [
    "Event",
]


class Event(BaseScope):
    """Methods for managing Bitrix24 event handler registrations.

    Documentation: https://apidocs.bitrix24.com/api-reference/events/index.html
    """

    @cached_property
    def offline(self) -> Offline:
        """Return the offline-event queue scope."""
        return Offline(self)

    @type_checker
    def bind(
            self,
            event: Text,
            handler: Text = MISSING,
            *,
            auth_type: int = MISSING,
            event_type: Annotated[Text, EventTypeLiteral] = MISSING,
            auth_connector: Text = MISSING,
            options: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Register a new event handler

        Documentation: https://apidocs.bitrix24.com/api-reference/events/event-bind.html

        The method registers a new event handler.

        Args:
            event: Event name;

            handler: Link to event handler;

            auth_type: Identifier of the user under whom the event handler is authorized;

            event_type: Value for online or offline event;

            auth_connector: Source key;

            options: Additional settings for the registered event;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "event": event,
        }

        if handler is not MISSING:
            params["handler"] = handler

        if auth_type is not MISSING:
            params["auth_type"] = auth_type

        if event_type is not MISSING:
            params["event_type"] = event_type

        if auth_connector is not MISSING:
            params["auth_connector"] = auth_connector

        if options is not MISSING:
            params["options"] = options

        return self._make_bitrix_api_request(
            api_wrapper=self.bind,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, EventObject]:
        """Return registered event handlers

        Documentation: https://apidocs.bitrix24.com/api-reference/events/event-get.html

        The method allows to retrieve a list of registered event handlers.

        Args:
            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter("event", client=self._client),
        )

    @type_checker
    def unbind(
            self,
            event: Text,
            handler: Text = MISSING,
            *,
            auth_type: int = MISSING,
            event_type: Annotated[Text, EventTypeLiteral] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[CountResultData, int]:
        """Unregister event handler

        Documentation: https://apidocs.bitrix24.com/api-reference/events/event-unbind.html

        The method unregisters a registered event handler.

        Args:
            event: Event name;

            handler: Link to event handler;

            auth_type: Identifier of the user under whom the event handler is authorized;

            event_type: Value for online or offline event;

            timeout: Timeout in seconds.

        Return:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "event": event,
        }

        if handler is not MISSING:
            params["handler"] = handler

        if auth_type is not MISSING:
            params["auth_type"] = auth_type

        if event_type is not MISSING:
            params["event_type"] = event_type

        return self._make_bitrix_api_request(
            api_wrapper=self.unbind,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixResultAdapter(int, wrapper="count"),
        )
