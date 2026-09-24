from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Generic, Text, TypeVar

from .._constants import MISSING
from ..utils.converters import int_from_bitrix, int_to_bitrix, text_from_bitrix, text_to_bitrix
from ..utils.dataclasses import frozen_dataclass_kwargs
from ..utils.types import JSONDict, JSONList, Self, Timeout
from ._base_object import BaseObject
from ._base_pk import BasePK
from ._fields import DictField, IntField, ObjectField, TextField, URLField
from ._managers import BaseObjectManager

if TYPE_CHECKING:
    from ..api.requests import BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ..client import ClientType
    from ..schemas.results import CountResultData
    from .user import User  # noqa: F401

__all__ = [
    "Placement",
    "PlacementManager",
    "PlacementPK",
]


@dataclass(**frozen_dataclass_kwargs())
class PlacementPK(BasePK):
    """Composite identifier of a registered Bitrix24 placement handler.

    Bitrix24 identifies a registered handler by its placement code, URL, and
    optional user ID. Application-wide handlers use ``user_id=0``.
    The API may still contain duplicate registrations with the same values;
    consequently, deleting one SDK object may remove several matching records.
    """

    placement: Text
    handler: Text
    user_id: int = 0

    def __post_init__(self):
        """Validate and normalize values passed to the public constructor."""

        if not isinstance(self.placement, str):
            self._set_value(
                "placement",
                text_from_bitrix(self.placement, is_required=True),
            )

        if not isinstance(self.handler, str):
            self._set_value(
                "handler",
                text_from_bitrix(self.handler, is_required=True),
            )

        if not isinstance(self.user_id, int) or isinstance(self.user_id, bool):
            self._set_value(
                "user_id",
                int_from_bitrix(self.user_id, is_required=True),
            )

        URLField.validate_url(self.handler)

    @classmethod
    def from_bitrix(cls, bitrix_data: JSONDict, /) -> "PlacementPK":
        """Create a placement key from raw ``placement.get`` data."""
        return cls(
            placement=bitrix_data["placement"],
            handler=bitrix_data["handler"],
            user_id=bitrix_data["userId"],
        )

    def to_bitrix(self) -> JSONDict:
        """Convert the key to raw ``placement.get`` field values."""
        return {
            "placement": text_to_bitrix(self.placement, is_required=True),
            "handler": text_to_bitrix(self.handler, is_required=True),
            "userId": int_to_bitrix(self.user_id, is_required=True),
        }


class Placement(BaseObject[PlacementPK]):
    """Handler registered at a Bitrix24 widget placement."""

    OBJECT_KEY = "placement"
    PK = PlacementPK

    objects: "PlacementManager[Self]"

    placement = TextField("placement", is_pk=True)
    handler = URLField("handler", is_pk=True)
    user_id = IntField("userId", is_pk=True)
    user = ObjectField["User"](user_id, object_class="user")
    options = DictField("options", is_updatable=False)
    title = TextField("title", is_updatable=False)
    description = TextField("description", is_updatable=False)
    lang_all = DictField("langAll", is_updatable=False)

    def _get_bitrix_data(self) -> JSONDict:
        """Load this placement-handler registration from Bitrix24."""

        placements = tuple(
            placement
            for placement in self.client.placement.get().values
            if placement.bitrix_pk == self.bitrix_pk
        )

        if not placements:
            raise self.DoesNotExist(
                f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.",
            )

        if len(placements) > 1:
            raise self.MultipleObjectsReturned(
                f"Multiple {self.__class__.__name__} objects returned for "
                f"pk={self.bitrix_pk!r}.",
            )

        return placements[0].bitrix_data

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Remove registrations matching this placement key."""
        return self._make_delete_request(timeout=timeout).value > 0

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[CountResultData, int]"]:
        """Return the placement-handler removal API method."""
        return client.placement.unbind

    def _make_delete_request(self, *, timeout: Timeout = None) -> "BitrixAPIValueRequest[CountResultData, int]":
        """Create a lazy unbind request from the composite key."""

        params: JSONDict = {
            "placement": self.placement,
            "handler": self.handler,
        }

        if self.user_id != 0:
            params["user_id"] = self.user_id

        return self._get_delete_api_wrapper(self.client)(**params, timeout=timeout)


_PlacementT = TypeVar("_PlacementT", bound=Placement)


class PlacementManager(BaseObjectManager[_PlacementT], Generic[_PlacementT]):
    """Manager for registered Bitrix24 placement handlers."""

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _PlacementT]"]:
        """Return the placement-handler list API method."""
        return client.placement.get

    def add(
            self,
            *,
            placement: Text,
            handler: Text,
            title: Text = MISSING,
            description: Text = MISSING,
            group_name: Text = MISSING,
            lang_all: JSONDict = MISSING,
            options: JSONDict = MISSING,
            user_id: int = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Register a placement handler and return the API success flag."""

        bind_params: JSONDict = {
            "placement": placement,
            "handler": handler,
        }

        if title is not MISSING:
            bind_params["title"] = title

        if description is not MISSING:
            bind_params["description"] = description

        if group_name is not MISSING:
            bind_params["group_name"] = group_name

        if lang_all is not MISSING:
            bind_params["lang_all"] = lang_all

        if options is not MISSING:
            bind_params["options"] = options

        if user_id is not MISSING:
            bind_params["user_id"] = user_id

        return self._client.placement.bind(**bind_params, timeout=timeout).result


Placement.objects = PlacementManager()
