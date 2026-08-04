from typing import TYPE_CHECKING, Any, Callable, Generic, Iterable, Optional, Text, TypeVar

from ...schemas.api import BitrixObjectBatchWriteResponse
from ...utils.types import JSONDict, JSONList, Self, Timeout
from .._base_object import BaseObject
from .._fields import BoolField, DictField, IntField, TextField
from .._managers import BaseObjectManager

if TYPE_CHECKING:
    from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ...client import ClientType
    from .._bitrix_object_list import BitrixObjectList

__all__ = [
    "UserUserfield",
    "UserUserfieldManager",
]


class UserUserfield(BaseObject[int]):
    """Bitrix24 user custom field definition."""

    _OBJECT_KEY = "user.userfield"
    _PK_TYPE = int

    objects: "UserUserfieldManager[Self]"

    bitrix_id = IntField("ID", is_pk=True)
    entity_id = TextField("ENTITY_ID")
    field_name = TextField("FIELD_NAME", is_required=True)
    user_type_id = TextField("USER_TYPE_ID", is_required=True)
    xml_id = TextField("XML_ID")
    sort = IntField("SORT")
    multiple = BoolField("MULTIPLE")
    mandatory = BoolField("MANDATORY")
    show_filter = TextField("SHOW_FILTER")
    show_in_list = BoolField("SHOW_IN_LIST")
    edit_in_list = BoolField("EDIT_IN_LIST")
    is_searchable = BoolField("IS_SEARCHABLE")
    settings = DictField("SETTINGS")
    list = DictField("LIST", is_multiple=True, is_missing_allowed=True)

    def _get_bitrix_data(self) -> JSONDict:
        """Load raw user custom field data from Bitrix24."""

        result = self.client.user.userfield.list(filter={"ID": self.bitrix_pk}).result

        if not result:
            raise self.DoesNotExist(f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.")

        if len(result) > 1:
            raise self.MultipleObjectsReturned(
                f"Multiple {self.__class__.__name__} objects returned for pk={self.bitrix_pk!r}.",
            )

        return result[0]

    def update(self, *, timeout: Timeout = None, **fields: Any) -> bool:
        """Update this user custom field in Bitrix24."""
        return self._update(**fields, timeout=timeout)

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the update API method resolved from the supplied client."""
        return client.user.userfield.update

    def save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save local user custom field changes to Bitrix24."""
        return self._save(update_fields=update_fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Delete this user custom field from Bitrix24."""
        return self._delete(timeout=timeout)

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the delete API method resolved from the supplied client."""
        return client.user.userfield.delete


_UserUserfieldT = TypeVar("_UserUserfieldT", bound=UserUserfield)


class UserUserfieldManager(BaseObjectManager[_UserUserfieldT], Generic[_UserUserfieldT]):
    """Query manager for Bitrix24 user custom fields."""

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _UserUserfieldT]"]:
        """Return the load API method resolved from the supplied client."""
        return client.user.userfield.list

    def filter(self, **filters: Any) -> Self:
        """Return user custom fields filtered by SDK object attribute names."""
        return self._filter(**filters)

    def order(self, *fields: Text) -> Self:
        """Return user custom fields ordered by SDK object attribute names."""
        return self._order(*fields)

    def start(self, start: Optional[int]) -> Self:
        """Return user custom fields with a custom Bitrix24 pagination start offset."""
        return self._start(start)

    def add(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> _UserUserfieldT:
        """Create a Bitrix24 user custom field."""
        return self._add(**fields, timeout=timeout)

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, _UserUserfieldT]"]:
        """Return the add API method resolved from the supplied client."""
        return client.user.userfield.add

    def add_many(
            self,
            items: Iterable[JSONDict],
            *,
            ignore_errors: bool = False,
            timeout: Timeout = None,
    ) -> "BitrixObjectList[_UserUserfieldT]":
        """Create many Bitrix24 user custom fields from SDK field dictionaries."""
        return self._add_many(
            items,
            ignore_errors=ignore_errors,
            timeout=timeout,
        )

    def update(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BitrixObjectBatchWriteResponse:
        """Update user custom fields matching the current query in batches."""
        return self._update(**fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> BitrixObjectBatchWriteResponse:
        """Delete user custom fields matching the current query in batches."""
        return self._delete(timeout=timeout)


UserUserfield.objects = UserUserfieldManager()
