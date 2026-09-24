from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Generic,
    Hashable,
    Iterable,
    Optional,
    Sequence,
    Text,
    Tuple,
    TypeVar,
    Union,
)

from ...._constants import MISSING
from ....constants.list import ListIBlockType
from ....utils.types import JSONDict, Self, Timeout
from ..._base_object import BaseObject
from ..._fields import BoolField, DictField, IntField, RawField, TextField
from ..._managers import BaseObjectManager
from ..._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult

if TYPE_CHECKING:
    from ....api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ....client import ClientType

__all__ = [
    "BaseListField",
    "BaseListFieldManager",
]


class BaseListField(BaseObject[Text]):
    """Shared object implementation for Bitrix24 list fields."""

    OBJECT_KEY = "list.field"
    PK = str

    IBLOCK_TYPE_ID: ClassVar[Optional[ListIBlockType]] = None
    IBLOCK_ID: ClassVar[Optional[int]] = None

    objects: "BaseListFieldManager[Self]"

    field_id = TextField("FIELD_ID", is_pk=True, request_name="field_id")
    sort = IntField("SORT")
    name = TextField("NAME", is_required=True)
    is_required = BoolField("IS_REQUIRED")
    multiple = BoolField("MULTIPLE")
    default_value = RawField("DEFAULT_VALUE")
    type = TextField("TYPE", is_required=True, is_updatable=False)
    property_type = TextField("PROPERTY_TYPE", is_read_only=True)
    property_user_type = RawField("PROPERTY_USER_TYPE", is_read_only=True)
    code = TextField("CODE")
    bitrix_id = TextField("ID", is_read_only=True)
    link_iblock_id = IntField("LINK_IBLOCK_ID")
    row_count = IntField("ROW_COUNT")
    col_count = IntField("COL_COUNT")
    user_type_settings = DictField("USER_TYPE_SETTINGS")
    settings = DictField("SETTINGS")
    display_values_form = DictField("DISPLAY_VALUES_FORM", is_read_only=True)
    list = DictField("LIST")
    list_text_values = TextField("LIST_TEXT_VALUES")
    list_def = IntField("LIST_DEF", is_multiple=True)

    @classmethod
    def get_discriminator(cls) -> Tuple[Optional[ListIBlockType], Optional[int]]:
        """Return the list type and list identifier used by the registry."""
        return cls.IBLOCK_TYPE_ID, cls.IBLOCK_ID

    @classmethod
    def get_required_class_params(cls) -> JSONDict:
        """Return the list identifiers required by field API methods."""
        return {
            "iblock_type_id": cls.IBLOCK_TYPE_ID,
            "iblock_id": cls.IBLOCK_ID,
        }

    def _get_bitrix_data(self) -> JSONDict:
        """Load complete field data from Bitrix24."""

        result = self.client.lists.field.get(**self._meta.required_class_params, field_id=self.bitrix_pk).result

        fields = list(result.values()) if isinstance(result, Mapping) else result

        if not fields:
            message = f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist."
            raise self.DoesNotExist(message)

        if len(fields) > 1:
            message = f"Multiple {self.__class__.__name__} objects returned for pk={self.bitrix_pk!r}."
            raise self.MultipleObjectsReturned(message)

        return fields[0]

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the list-field update API method."""
        return client.lists.field.update

    def update(
            self,
            *,
            name: Text = MISSING,
            is_required: bool = MISSING,
            multiple: bool = MISSING,
            sort: int = MISSING,
            default_value: Any = MISSING,
            list: JSONDict = MISSING,
            list_text_values: Text = MISSING,
            list_def: Iterable[int] = MISSING,
            code: Text = MISSING,
            settings: JSONDict = MISSING,
            user_type_settings: JSONDict = MISSING,
            row_count: int = MISSING,
            col_count: int = MISSING,
            link_iblock_id: int = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Update supported settings of this list field."""

        fields = {
            key: value
            for key, value in (
                ("name", name),
                ("is_required", is_required),
                ("multiple", multiple),
                ("sort", sort),
                ("default_value", default_value),
                ("list", list),
                ("list_text_values", list_text_values),
                ("list_def", list_def),
                ("code", code),
                ("settings", settings),
                ("user_type_settings", user_type_settings),
                ("row_count", row_count),
                ("col_count", col_count),
                ("link_iblock_id", link_iblock_id),
            )
            if value is not MISSING
        }

        return self._update(**fields, timeout=timeout)

    def save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save local changes or selected current field settings."""
        return self._save(update_fields=update_fields, timeout=timeout)

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the list-field delete API method."""
        return client.lists.field.delete

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Delete this field from its Bitrix24 list."""
        return self._delete(timeout=timeout)


_BaseListFieldT = TypeVar("_BaseListFieldT", bound=BaseListField)


class BaseListFieldManager(BaseObjectManager[_BaseListFieldT], Generic[_BaseListFieldT]):
    """Query and creation manager shared by all list field types."""

    _FILTER_KEY = None
    _ORDER_KEY = None

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONDict, _BaseListFieldT]"]:
        """Return the list-field retrieval API method."""
        return client.lists.field.get

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[Text, _BaseListFieldT]"]:
        """Return the list-field creation API method."""
        return client.lists.field.add

    def filter(self, *, field_id: Text) -> Self:
        """Return the field with the supplied identifier."""
        return self._filter(field_id=field_id)

    def from_pks(self, bitrix_pks: Iterable[Text]) -> Self:
        """Return fields whose identifiers belong to the supplied iterable."""
        return self._from_pks(bitrix_pks)

    def add(
            self,
            *,
            name: Text,
            type: Text,
            is_required: bool = MISSING,
            multiple: bool = MISSING,
            sort: int = MISSING,
            default_value: Any = MISSING,
            list: JSONDict = MISSING,
            list_text_values: Text = MISSING,
            list_def: Iterable[int] = MISSING,
            code: Text = MISSING,
            settings: JSONDict = MISSING,
            user_type_settings: JSONDict = MISSING,
            row_count: int = MISSING,
            col_count: int = MISSING,
            link_iblock_id: int = MISSING,
            timeout: Timeout = None,
    ) -> _BaseListFieldT:
        """Create a field in the manager's fixed Bitrix24 list."""

        fields = {
            key: value
            for key, value in (
                ("name", name),
                ("type", type),
                ("is_required", is_required),
                ("multiple", multiple),
                ("sort", sort),
                ("default_value", default_value),
                ("list", list),
                ("list_text_values", list_text_values),
                ("list_def", list_def),
                ("code", code),
                ("settings", settings),
                ("user_type_settings", user_type_settings),
                ("row_count", row_count),
                ("col_count", col_count),
                ("link_iblock_id", link_iblock_id),
            )
            if value is not MISSING
        }

        return self._add(**fields, timeout=timeout)

    def add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[_BaseListFieldT]:
        """Create multiple list fields through the client's batch API."""
        return self._add_many(objects_data, timeout=timeout)

    def update(
            self,
            *,
            name: Text = MISSING,
            is_required: bool = MISSING,
            multiple: bool = MISSING,
            sort: int = MISSING,
            default_value: Any = MISSING,
            list: JSONDict = MISSING,
            list_text_values: Text = MISSING,
            list_def: Iterable[int] = MISSING,
            code: Text = MISSING,
            settings: JSONDict = MISSING,
            user_type_settings: JSONDict = MISSING,
            row_count: int = MISSING,
            col_count: int = MISSING,
            link_iblock_id: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResult[_BaseListFieldT]:
        """Update list fields matching the current query."""

        fields = {
            key: value
            for key, value in (
                ("name", name),
                ("is_required", is_required),
                ("multiple", multiple),
                ("sort", sort),
                ("default_value", default_value),
                ("list", list),
                ("list_text_values", list_text_values),
                ("list_def", list_def),
                ("code", code),
                ("settings", settings),
                ("user_type_settings", user_type_settings),
                ("row_count", row_count),
                ("col_count", col_count),
                ("link_iblock_id", link_iblock_id),
            )
            if value is not MISSING
        }

        return self._update(**fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> BitrixObjectBatchWriteResult[_BaseListFieldT]:
        """Delete list fields matching the current query."""
        return self._delete(timeout=timeout)
