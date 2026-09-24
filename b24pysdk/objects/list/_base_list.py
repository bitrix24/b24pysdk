from typing import TYPE_CHECKING, Callable, ClassVar, Generic, Hashable, Iterable, Mapping, Optional, Sequence, Text, TypeVar, Union

from ..._constants import MISSING
from ...constants.list import ListIBlockType
from ...utils.types import JSONDict, JSONList, Self, Timeout
from .._base_object import BaseObject
from .._fields import BoolField, DictField, EnumField, IntField, TextField
from .._managers import BaseObjectManager
from .._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult

if TYPE_CHECKING:
    from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ...client import ClientType

__all__ = [
    "BaseList",
    "BaseListManager",
]


class BaseList(BaseObject[int]):
    """Shared object implementation for Bitrix24 list types."""

    OBJECT_KEY = "list"
    PK = int
    IBLOCK_TYPE_ID: ClassVar[Optional[ListIBlockType]] = None

    objects: "BaseListManager[Self]"

    bitrix_id = IntField("ID", request_name="iblock_id", is_pk=True)
    timestamp_x = TextField("TIMESTAMP_X", is_read_only=True)
    iblock_type_id = EnumField[ListIBlockType]("IBLOCK_TYPE_ID", enum_class=ListIBlockType, is_required=True, is_read_only=True)
    lid = TextField("LID", is_read_only=True)
    code = TextField("CODE", is_updatable=False, request_name="iblock_code")
    api_code = TextField("API_CODE", is_read_only=True)
    name = TextField("NAME", is_required=True)
    active = BoolField("ACTIVE", is_read_only=True)
    sort = IntField("SORT")
    list_page_url = TextField("LIST_PAGE_URL", is_read_only=True)
    detail_page_url = TextField("DETAIL_PAGE_URL", is_read_only=True)
    section_page_url = TextField("SECTION_PAGE_URL", is_read_only=True)
    canonical_page_url = TextField("CANONICAL_PAGE_URL", is_read_only=True)
    description = TextField("DESCRIPTION")
    description_type = TextField("DESCRIPTION_TYPE", is_read_only=True)
    rss_ttl = IntField("RSS_TTL", is_read_only=True)
    rss_active = BoolField("RSS_ACTIVE", is_read_only=True)
    rss_file_active = BoolField("RSS_FILE_ACTIVE", is_read_only=True)
    rss_file_limit = IntField("RSS_FILE_LIMIT", is_read_only=True)
    rss_file_days = IntField("RSS_FILE_DAYS", is_read_only=True)
    rss_yandex_active = BoolField("RSS_YANDEX_ACTIVE", is_read_only=True)
    xml_id = TextField("XML_ID", is_read_only=True)
    tmp_id = TextField("TMP_ID", is_read_only=True)
    index_element = BoolField("INDEX_ELEMENT", is_read_only=True)
    index_section = BoolField("INDEX_SECTION", is_read_only=True)
    workflow = BoolField("WORKFLOW", is_read_only=True)
    bizproc = BoolField("BIZPROC")
    section_chooser = TextField("SECTION_CHOOSER", is_read_only=True)
    list_mode = TextField("LIST_MODE", is_read_only=True)
    messages = DictField("MESSAGES")
    rights = DictField("RIGHTS")
    section_property = BoolField("SECTION_PROPERTY", is_read_only=True)
    property_index = BoolField("PROPERTY_INDEX", is_read_only=True)
    version = IntField("VERSION", is_read_only=True)
    last_conv_element = IntField("LAST_CONV_ELEMENT", is_read_only=True)
    socnet_group_id = IntField("SOCNET_GROUP_ID")
    edit_file_before = TextField("EDIT_FILE_BEFORE", is_read_only=True)
    edit_file_after = TextField("EDIT_FILE_AFTER", is_read_only=True)
    sections_name = TextField("SECTIONS_NAME", is_updatable=False)
    section_name = TextField("SECTION_NAME", is_updatable=False)
    elements_name = TextField("ELEMENTS_NAME", is_updatable=False)
    element_name = TextField("ELEMENT_NAME", is_updatable=False)
    rest_on = BoolField("REST_ON", is_read_only=True)
    fulltext_index = BoolField("FULLTEXT_INDEX", is_read_only=True)
    external_id = TextField("EXTERNAL_ID", is_read_only=True)
    lang_dir = TextField("LANG_DIR", is_read_only=True)
    server_name = TextField("SERVER_NAME", is_read_only=True)

    @classmethod
    def get_discriminator(cls) -> Optional[ListIBlockType]:
        """Return the information-block type used to register this list class."""
        return cls.IBLOCK_TYPE_ID

    @classmethod
    def get_required_class_params(cls) -> JSONDict:
        """Return the information-block type required by list API methods."""
        return {"iblock_type_id": cls.IBLOCK_TYPE_ID}

    def _get_bitrix_data(self) -> JSONDict:
        """Load complete list data from Bitrix24."""

        lists = self.client.lists.get(
            **self._meta.required_class_params,
            iblock_id=self.bitrix_pk,
        ).result

        if not lists:
            raise self.DoesNotExist(
                f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.",
            )

        if len(lists) > 1:
            raise self.MultipleObjectsReturned(
                f"Multiple {self.__class__.__name__} objects returned "
                f"for pk={self.bitrix_pk!r}.",
            )

        return lists[0]

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the list update API method."""
        return client.lists.update

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the list delete API method."""
        return client.lists.delete

    def _get_update_params(self, updated_data: JSONDict) -> JSONDict:
        """Move endpoint-specific values outside the list fields mapping."""

        endpoint_fields = ("SOCNET_GROUP_ID", "MESSAGES", "RIGHTS")

        not_endpoint_params = {
            key: value
            for key, value in updated_data.items()
            if key not in endpoint_fields
        }

        params = super()._get_update_params(not_endpoint_params)

        for bitrix_code in endpoint_fields:
            if bitrix_code in updated_data:
                field = self._meta.get_field_by_bitrix_code(bitrix_code)
                params[field.request_name] = updated_data[bitrix_code]

        return params

    def update(
            self,
            *,
            name: Text = MISSING,
            description: Text = MISSING,
            sort: int = MISSING,
            bizproc: bool = MISSING,
            socnet_group_id: int = MISSING,
            messages: JSONDict = MISSING,
            rights: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Update this list in Bitrix24."""

        fields = {
            key: value
            for key, value in (
                ("name", name),
                ("description", description),
                ("sort", sort),
                ("bizproc", bizproc),
                ("socnet_group_id", socnet_group_id),
                ("messages", messages),
                ("rights", rights),
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
        """Save local changes or selected current list fields to Bitrix24."""
        return self._save(update_fields=update_fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Delete this list from Bitrix24."""
        return self._delete(timeout=timeout)


_BaseListT = TypeVar("_BaseListT", bound=BaseList)


class BaseListManager(BaseObjectManager[_BaseListT], Generic[_BaseListT]):
    """Query and creation manager shared by all Bitrix24 list types."""

    _FILTER_KEY = None
    _ORDER_KEY = "iblock_order"

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _BaseListT]"]:
        """Return the universal-list retrieval API method."""
        return client.lists.get

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, _BaseListT]"]:
        """Return the list creation API method."""
        return client.lists.add

    def _get_add_params(
            self,
            fields: JSONDict,
            *,
            add_params: Optional[JSONDict] = None,
    ) -> JSONDict:
        """Move the required list code outside the list fields mapping."""

        if "iblock_code" not in fields:
            raise ValueError("Pass iblock_code to add a list.") from None

        endpoint_fields = ("iblock_code", "socnet_group_id", "messages", "rights")

        not_endpoint_params = {
            key: value
            for key, value in fields.items()
            if key not in endpoint_fields
        }

        params = super()._get_add_params(not_endpoint_params, add_params=add_params)

        for field_name in endpoint_fields:
            if field_name in fields:
                params[field_name] = fields[field_name]

        return params

    def filter(
            self,
            *,
            bitrix_id: int = MISSING,
            code: Text = MISSING,
            socnet_group_id: int = MISSING,
    ) -> Self:
        """Return lists matching supported exact lookup parameters."""

        filters: JSONDict = {}

        if bitrix_id is not MISSING:
            filters["bitrix_id"] = bitrix_id

        if code is not MISSING:
            filters["code"] = code

        if socnet_group_id is not MISSING:
            filters["socnet_group_id"] = socnet_group_id

        return self._filter(**filters)

    def order(self, *fields: Text) -> Self:
        """Return lists ordered by fields supported by ``lists.get``."""
        return self._order(*fields)

    def start(self, start: Optional[int]) -> Self:
        """Return lists with a custom pagination start offset."""
        return self._start(start)

    def from_pks(self, bitrix_pks: Iterable[int]) -> Self:
        """Return lists whose identifiers belong to the supplied iterable."""
        return self._from_pks(bitrix_pks)

    def add(
            self,
            *,
            iblock_code: Text,
            name: Text,
            description: Text = MISSING,
            sort: int = MISSING,
            bizproc: bool = MISSING,
            socnet_group_id: int = MISSING,
            messages: JSONDict = MISSING,
            rights: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> _BaseListT:
        """Create a list of the manager's fixed Bitrix24 type."""

        fields = {
            key: value
            for key, value in (
                ("iblock_code", iblock_code),
                ("name", name),
                ("description", description),
                ("sort", sort),
                ("bizproc", bizproc),
                ("socnet_group_id", socnet_group_id),
                ("messages", messages),
                ("rights", rights),
            )
            if value is not MISSING
        }

        return self._add(**fields, timeout=timeout)

    def add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[_BaseListT]:
        """Create multiple lists through the client's batch API."""
        return self._add_many(objects_data, timeout=timeout)

    def update(
            self,
            *,
            name: Text = MISSING,
            description: Text = MISSING,
            sort: int = MISSING,
            bizproc: bool = MISSING,
            socnet_group_id: int = MISSING,
            messages: JSONDict = MISSING,
            rights: JSONDict = MISSING,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResult[_BaseListT]:
        """Update lists matching the current query in batches."""

        fields = {
            key: value
            for key, value in (
                ("name", name),
                ("description", description),
                ("sort", sort),
                ("bizproc", bizproc),
                ("socnet_group_id", socnet_group_id),
                ("messages", messages),
                ("rights", rights),
            )
            if value is not MISSING
        }

        return self._update(**fields, timeout=timeout)

    def delete(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResult[_BaseListT]:
        """Delete lists matching the current query in batches."""
        return self._delete(timeout=timeout)
