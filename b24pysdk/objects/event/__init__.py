from dataclasses import dataclass
from typing import TYPE_CHECKING, Annotated, Callable, Generic, Optional, Text, TypeVar

from ..._constants import MISSING
from ...constants.event import EventTypeLiteral
from ...utils.converters import (
    bool_from_bitrix,
    bool_to_bitrix,
    int_from_bitrix,
    int_to_bitrix,
    text_from_bitrix,
    text_to_bitrix,
)
from ...utils.dataclasses import frozen_dataclass_kwargs
from ...utils.types import JSONDict, JSONList, Self, Timeout
from .._base_object import BaseObject
from .._base_pk import BasePK
from .._fields import BoolField, IntField, TextField, URLField
from .._managers import BaseObjectManager

if TYPE_CHECKING:
    from ...api.requests import BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ...client import ClientType
    from ...schemas.results import CountResultData

__all__ = [
    "Event",
    "EventManager",
    "EventPK",
]


@dataclass(**frozen_dataclass_kwargs())
class EventPK(BasePK):
    """Composite identifier of a registered Bitrix24 event handler."""

    event: Text
    offline: bool
    handler: Optional[Text] = None
    auth_type: Optional[int] = None

    def __post_init__(self):
        """Validate values supplied through the public Python constructor."""

        if not isinstance(self.event, str):
            self._set_value(
                "event",
                text_from_bitrix(self.event, is_required=True),
            )

        if not isinstance(self.offline, bool):
            self._set_value(
                "offline",
                bool_from_bitrix(self.offline, is_required=True),
            )

        if not isinstance(self.auth_type, int) or isinstance(self.auth_type, bool):
            self._set_value(
                "auth_type",
                int_from_bitrix(self.auth_type, is_required=False),
            )

        if self.offline:
            self._set_value("handler", None)

        elif self.handler is None:
            raise ValueError("handler is required for an online event.")

        elif not isinstance(self.handler, str):
            self._set_value(
                "handler",
                text_from_bitrix(self.handler, is_required=True),
            )

        if self.handler is not None:
            URLField.validate_url(self.handler)

    @classmethod
    def from_bitrix(cls, bitrix_data: JSONDict, /) -> "EventPK":
        """Create an event key from raw ``event.get`` data."""
        return cls(
            event=bitrix_data["event"],
            handler=bitrix_data.get("handler"),
            auth_type=bitrix_data.get("auth_type"),
            offline=bitrix_data["offline"],
        )

    def to_bitrix(self) -> JSONDict:
        """Convert the event key to raw ``event.get`` field values."""
        return {
            "event": text_to_bitrix(self.event, is_required=True),
            "handler": text_to_bitrix(self.handler),
            "auth_type": int_to_bitrix(self.auth_type),
            "offline": bool_to_bitrix(self.offline, is_required=True, serialize_as=int),
        }


class Event(BaseObject[EventPK]):
    """Bitrix24 event handler registration."""

    OBJECT_KEY = "event"
    PK = EventPK

    objects: "EventManager[Self]"

    event = TextField("event", is_pk=True)
    handler = URLField("handler", is_pk=True, is_required=False)
    auth_type = IntField("auth_type", is_pk=True, is_required=False)
    offline = BoolField("offline", is_pk=True, serialize_as=int)

    def _get_bitrix_data(self) -> JSONDict:
        """Load this event handler registration from Bitrix24."""

        events = tuple(
            event
            for event in self.client.event.get().values
            if event.bitrix_pk == self.bitrix_pk
        )

        if not events:
            raise self.DoesNotExist(
                f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.",
            )

        if len(events) > 1:
            raise self.MultipleObjectsReturned(
                f"Multiple {self.__class__.__name__} objects returned for "
                f"pk={self.bitrix_pk!r}.",
            )

        return events[0].bitrix_data

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Unregister this event handler in Bitrix24."""
        return self._make_delete_request(timeout=timeout).value > 0

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[CountResultData, int]"]:
        """Return the event-handler removal API method."""
        return client.event.unbind

    def _make_delete_request(self, *, timeout: Timeout = None) -> "BitrixAPIValueRequest[CountResultData, int]":
        """Create a lazy unbind request from this event's composite key."""

        params: JSONDict = {
            "event": self.event,
            "event_type": "offline" if self.offline else "online",
        }

        if self.handler is not None:
            params["handler"] = self.handler

        if self.auth_type is not None:
            params["auth_type"] = self.auth_type

        return self._get_delete_api_wrapper(self.client)(**params, timeout=timeout)


_EventT = TypeVar("_EventT", bound=Event)


class EventManager(BaseObjectManager[_EventT], Generic[_EventT]):
    """Manager for registered Bitrix24 event handlers."""

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _EventT]"]:
        """Return the event-handler list API method."""
        return client.event.get

    def add(
            self,
            *,
            event: Text,
            handler: Text = MISSING,
            auth_type: int = MISSING,
            event_type: Annotated[Text, EventTypeLiteral] = MISSING,
            auth_connector: Text = MISSING,
            options: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Register an event handler and return the API success flag."""

        bind_params: JSONDict = {
            "event": event,
        }

        if handler is not MISSING:
            bind_params["handler"] = handler

        if auth_type is not MISSING:
            bind_params["auth_type"] = auth_type

        if event_type is not MISSING:
            bind_params["event_type"] = event_type

        if auth_connector is not MISSING:
            bind_params["auth_connector"] = auth_connector

        if options is not MISSING:
            bind_params["options"] = options

        return self._client.event.bind(**bind_params, timeout=timeout).result


Event.objects = EventManager()
