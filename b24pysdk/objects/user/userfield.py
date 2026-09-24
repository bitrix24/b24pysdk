from typing import TYPE_CHECKING, Any, Callable, Generic, Hashable, Iterable, List, Mapping, Optional, Sequence, Text, TypeVar, Union

from ..._constants import MISSING
from ...schemas.user.userfield import UserUserfieldListItem
from ...utils.types import JSONDict, JSONList, Self, Timeout
from .._base_object import BaseObject
from .._fields import BitrixSchemaField, BoolField, DictField, IntField, TextField
from .._managers import BaseObjectManager
from .._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult

if TYPE_CHECKING:
    from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ...client import ClientType

__all__ = [
    "UserUserfield",
    "UserUserfieldManager",
]


class UserUserfield(BaseObject[int]):
    """Bitrix24 user custom field definition."""

    OBJECT_KEY = "user.userfield"
    PK = int

    objects: "UserUserfieldManager[Self]"

    bitrix_id = IntField("ID", is_pk=True)
    entity_id = TextField("ENTITY_ID", is_required=True, is_read_only=True)
    field_name = TextField("FIELD_NAME", is_required=True, is_updatable=False)
    user_type_id = TextField("USER_TYPE_ID", is_required=True, is_updatable=False)
    xml_id = TextField("XML_ID")
    sort = IntField("SORT", is_required=True)
    multiple = BoolField("MULTIPLE", is_required=True, is_updatable=False)
    mandatory = BoolField("MANDATORY", is_required=True)
    show_filter = BoolField("SHOW_FILTER", is_required=True)
    show_in_list = BoolField("SHOW_IN_LIST", is_required=True)
    edit_in_list = BoolField("EDIT_IN_LIST", is_required=True)
    is_searchable = BoolField("IS_SEARCHABLE", is_required=True)
    settings = DictField("SETTINGS", is_required=True)
    user_type_owner = TextField("USER_TYPE_OWNER", is_read_only=True)
    list = BitrixSchemaField[UserUserfieldListItem]("LIST", schema_class=UserUserfieldListItem, is_multiple=True)

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

    def update(
            self,
            *,
            xml_id: Optional[Text] = MISSING,
            sort: int = MISSING,
            mandatory: bool = MISSING,
            show_filter: bool = MISSING,
            show_in_list: bool = MISSING,
            edit_in_list: bool = MISSING,
            is_searchable: bool = MISSING,
            settings: JSONDict = MISSING,
            list: List[UserUserfieldListItem] = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Update this user custom field in Bitrix24."""

        fields: JSONDict = {}

        if xml_id is not MISSING:
            fields["xml_id"] = xml_id

        if sort is not MISSING:
            fields["sort"] = sort

        if mandatory is not MISSING:
            fields["mandatory"] = mandatory

        if show_filter is not MISSING:
            fields["show_filter"] = show_filter

        if show_in_list is not MISSING:
            fields["show_in_list"] = show_in_list

        if edit_in_list is not MISSING:
            fields["edit_in_list"] = edit_in_list

        if is_searchable is not MISSING:
            fields["is_searchable"] = is_searchable

        if settings is not MISSING:
            fields["settings"] = settings

        if list is not MISSING:
            fields["list"] = list

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
        """Save local changes or selected current custom field values to Bitrix24."""
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

    def from_pks(self, bitrix_pks: Iterable[int]) -> Self:
        """Return user custom fields filtered by Bitrix24 primary keys."""
        return self._from_pks(bitrix_pks)

    def order(self, *fields: Text) -> Self:
        """Return user custom fields ordered by SDK object attribute names."""
        return self._order(*fields)

    def add(  # noqa: C901
            self,
            *,
            field_name: Text,
            user_type_id: Text,
            xml_id: Optional[Text] = MISSING,
            sort: int = MISSING,
            multiple: bool = MISSING,
            mandatory: bool = MISSING,
            show_filter: bool = MISSING,
            show_in_list: bool = MISSING,
            edit_in_list: bool = MISSING,
            is_searchable: bool = MISSING,
            settings: JSONDict = MISSING,
            list: List[UserUserfieldListItem] = MISSING,
            timeout: Timeout = None,
    ) -> _UserUserfieldT:
        """Create a Bitrix24 user custom field."""

        fields: JSONDict = {
            "field_name": field_name,
            "user_type_id": user_type_id,
        }

        if xml_id is not MISSING:
            fields["xml_id"] = xml_id

        if sort is not MISSING:
            fields["sort"] = sort

        if multiple is not MISSING:
            fields["multiple"] = multiple

        if mandatory is not MISSING:
            fields["mandatory"] = mandatory

        if show_filter is not MISSING:
            fields["show_filter"] = show_filter

        if show_in_list is not MISSING:
            fields["show_in_list"] = show_in_list

        if edit_in_list is not MISSING:
            fields["edit_in_list"] = edit_in_list

        if is_searchable is not MISSING:
            fields["is_searchable"] = is_searchable

        if settings is not MISSING:
            fields["settings"] = settings

        if list is not MISSING:
            fields["list"] = list

        return self._add(**fields, timeout=timeout)

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, _UserUserfieldT]"]:
        """Return the add API method resolved from the supplied client."""
        return client.user.userfield.add

    def add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[_UserUserfieldT]:
        """Create many Bitrix24 user custom fields from SDK field dictionaries."""
        return self._add_many(objects_data, timeout=timeout)

    def update(
            self,
            *,
            xml_id: Optional[Text] = MISSING,
            sort: int = MISSING,
            mandatory: bool = MISSING,
            show_filter: bool = MISSING,
            show_in_list: bool = MISSING,
            edit_in_list: bool = MISSING,
            is_searchable: bool = MISSING,
            settings: JSONDict = MISSING,
            list: List[UserUserfieldListItem] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResult[_UserUserfieldT]:
        """Update user custom fields matching the current query in batches."""

        fields: JSONDict = {}

        if xml_id is not MISSING:
            fields["xml_id"] = xml_id

        if sort is not MISSING:
            fields["sort"] = sort

        if mandatory is not MISSING:
            fields["mandatory"] = mandatory

        if show_filter is not MISSING:
            fields["show_filter"] = show_filter

        if show_in_list is not MISSING:
            fields["show_in_list"] = show_in_list

        if edit_in_list is not MISSING:
            fields["edit_in_list"] = edit_in_list

        if is_searchable is not MISSING:
            fields["is_searchable"] = is_searchable

        if settings is not MISSING:
            fields["settings"] = settings

        if list is not MISSING:
            fields["list"] = list

        return self._update(**fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> BitrixObjectBatchWriteResult[_UserUserfieldT]:
        """Delete user custom fields matching the current query in batches."""
        return self._delete(timeout=timeout)


UserUserfield.objects = UserUserfieldManager()
