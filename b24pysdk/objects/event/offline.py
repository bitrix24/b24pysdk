from typing import TYPE_CHECKING, Any, Callable, Generic, Iterable, Optional, Text, TypeVar

from ..._constants import MISSING
from ...utils.types import JSONDict, JSONList, Self, Timeout
from .._base_object import BaseObject
from .._fields import BoolField, DateTimeField, DictField, IntField, TextField
from .._managers import BaseObjectManager

if TYPE_CHECKING:
    from ...api.requests import BitrixAPIValuesRequest
    from ...client import ClientType

__all__ = [
    "OfflineEvent",
    "OfflineEventManager",
]


class OfflineEvent(BaseObject[int]):
    """Read-only event stored in the Bitrix24 offline-event queue."""

    OBJECT_KEY = "event.offline"
    PK = int

    objects: "OfflineEventManager[Self]"

    bitrix_id = IntField("ID", is_pk=True)
    timestamp_x = DateTimeField("TIMESTAMP_X", is_required=True)
    event_name = TextField("EVENT_NAME", is_required=True)
    event_data = DictField("EVENT_DATA")
    event_additional = DictField("EVENT_ADDITIONAL")
    message_id = IntField("MESSAGE_ID", is_required=True)
    process_id = TextField("PROCESS_ID")
    error = BoolField("ERROR", serialize_as=int)

    def _get_bitrix_data(self) -> JSONDict:
        """Load this offline event without changing the queue state."""

        events = self.client.event.offline.list(
            filter={"ID": self.bitrix_pk},
        ).result

        if not events:
            raise self.DoesNotExist(
                f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.",
            )

        if len(events) > 1:
            raise self.MultipleObjectsReturned(
                f"Multiple {self.__class__.__name__} objects returned for "
                f"pk={self.bitrix_pk!r}.",
            )

        return events[0]


_OfflineEventT = TypeVar("_OfflineEventT", bound=OfflineEvent)


class OfflineEventManager(BaseObjectManager[_OfflineEventT], Generic[_OfflineEventT]):
    """Query manager for the Bitrix24 offline-event queue."""

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _OfflineEventT]"]:
        """Return the non-destructive offline-event list API method."""
        return client.event.offline.list

    def filter(self, **filters: Any) -> Self:
        """Return a manager copy with offline-event filters."""
        return self._filter(**filters)

    def from_pks(self, bitrix_pks: Iterable[int]) -> Self:
        """Return a manager copy filtered by offline-event IDs."""
        return self._from_pks(bitrix_pks)

    def order(self, *fields: Text) -> Self:
        """Return a manager copy ordered by offline-event fields."""
        return self._order(*fields)

    def start(self, start: Optional[int]) -> Self:
        """Return a manager copy with a pagination offset."""
        return self._start(start)

    def with_auth_connector(self, auth_connector: Text) -> Self:
        """Return a query with the ``auth_connector`` request parameter."""
        return self._with_params(auth_connector=auth_connector)

    def get(
            self,
            *,
            limit: int = MISSING,
            clear: bool = MISSING,
            process_id: Text = MISSING,
            auth_connector: Text = MISSING,
            error: bool = MISSING,
    ) -> Self:
        """Return a query that reserves events through ``event.offline.get``."""

        params: JSONDict = {}

        if limit is not MISSING:
            params["limit"] = limit

        if clear is not MISSING:
            params["clear"] = clear

        if process_id is not MISSING:
            params["process_id"] = process_id

        if auth_connector is not MISSING:
            params["auth_connector"] = auth_connector

        if error is not MISSING:
            params["error"] = error

        manager = self if not params else self._with_params(**params)

        return manager._with_api_wrapper(
            lambda client: client.event.offline.get,
        ).all()

    def clear(
            self,
            process_id: Text,
            *,
            bitrix_id: Iterable[int] = MISSING,
            message_id: Iterable[int] = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Clear records from a reserved offline-event package."""
        return self._client.event.offline.clear(
            process_id,
            bitrix_id=bitrix_id,
            message_id=message_id,
            timeout=timeout,
        ).result

    def error(
            self,
            process_id: Text,
            *,
            message_id: Iterable[int] = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Mark records from a reserved offline-event package as erroneous."""
        return self._client.event.offline.error(
            process_id,
            message_id=message_id,
            timeout=timeout,
        ).result


OfflineEvent.objects = OfflineEventManager()
