from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Generic,
    Hashable,
    Iterable,
    Mapping,
    Optional,
    Sequence,
    Text,
    Tuple,
    TypeVar,
    Union,
)

from ...._constants import MISSING
from ....constants.list import ListIBlockType
from ....utils.types import JSONDict, JSONList, Self, Timeout
from ..._base_object import BaseObject
from ..._fields import BoolField, DateTimeField, IntField, ObjectField, TextField
from ..._fields.raw_field import RawField
from ..._filter_lookups import FilterLookup
from ..._managers import BaseObjectManager
from ..._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult

if TYPE_CHECKING:
    from ....api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ....client import ClientType
    from ...user import User  # noqa: F401

__all__ = [
    "BaseListSection",
    "BaseListSectionManager",
]


class BaseListSection(BaseObject[int]):
    """Shared object implementation for Bitrix24 list sections."""

    OBJECT_KEY = "list.section"
    PK = int

    _FILTER_LOOKUPS = frozenset({
        FilterLookup.NOT_EXACT,
        FilterLookup.GT,
        FilterLookup.GTE,
        FilterLookup.LT,
        FilterLookup.LTE,
        FilterLookup.CONTAINS,
    })

    IBLOCK_TYPE_ID: ClassVar[Optional[ListIBlockType]] = None
    IBLOCK_ID: ClassVar[Optional[int]] = None

    objects: "BaseListSectionManager[Self]"

    bitrix_id = IntField("ID", is_pk=True, request_name="section_id")
    code = TextField("CODE", is_required=True, is_updatable=False, request_name="section_code")
    xml_id = TextField("XML_ID")
    external_id = TextField("EXTERNAL_ID")
    parent_section_id = IntField("IBLOCK_SECTION_ID", is_updatable=False, request_name="iblock_section_id")
    timestamp_x = DateTimeField("TIMESTAMP_X", is_read_only=True)
    sort = IntField("SORT")
    name = TextField("NAME", is_required=True)
    active = BoolField("ACTIVE")
    global_active = BoolField("GLOBAL_ACTIVE", is_read_only=True)
    picture = RawField("PICTURE", is_read_only=True)
    description = TextField("DESCRIPTION")
    description_type = TextField("DESCRIPTION_TYPE")
    left_margin = IntField("LEFT_MARGIN", is_read_only=True)
    right_margin = IntField("RIGHT_MARGIN", is_read_only=True)
    depth_level = IntField("DEPTH_LEVEL", is_read_only=True)
    searchable_content = TextField("SEARCHABLE_CONTENT", is_read_only=True)
    section_page_url = TextField("SECTION_PAGE_URL", is_read_only=True)
    modified_by_id = IntField("MODIFIED_BY", is_read_only=True)
    modified_by = ObjectField["User"](modified_by_id, object_class="user")
    date_create = DateTimeField("DATE_CREATE", is_read_only=True)
    created_by_id = IntField("CREATED_BY", is_read_only=True)
    created_by = ObjectField["User"](created_by_id, object_class="user")
    detail_picture = RawField("DETAIL_PICTURE", is_read_only=True)

    @classmethod
    def get_discriminator(cls) -> Tuple[Optional[ListIBlockType], Optional[int]]:
        """Return the list type and list identifier used by the registry."""
        return cls.IBLOCK_TYPE_ID, cls.IBLOCK_ID

    @classmethod
    def get_required_class_params(cls) -> JSONDict:
        """Return the list identifiers required by section API methods."""
        return {
            "iblock_type_id": cls.IBLOCK_TYPE_ID,
            "iblock_id": cls.IBLOCK_ID,
        }

    def _get_bitrix_data(self) -> JSONDict:
        """Load complete section data from Bitrix24."""

        class_params = self._meta.required_class_params
        sections = self.client.lists.section.get(**class_params, filter={"ID": self.bitrix_pk}).result

        if not sections:
            message = f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist."
            raise self.DoesNotExist(message)

        if len(sections) > 1:
            message = f"Multiple {self.__class__.__name__} objects returned for pk={self.bitrix_pk!r}."
            raise self.MultipleObjectsReturned(message)

        return sections[0]

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the list-section update API method."""
        return client.lists.section.update

    def update(self, *, timeout: Timeout = None, **fields: Any) -> bool:
        """Update this section in Bitrix24."""
        return self._update(**fields, timeout=timeout)

    def save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save local section changes to Bitrix24."""
        return self._save(update_fields=update_fields, timeout=timeout)

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the list-section delete API method."""
        return client.lists.section.delete

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Delete this section from Bitrix24."""
        return self._delete(timeout=timeout)


_BaseListSectionT = TypeVar("_BaseListSectionT", bound=BaseListSection)


class BaseListSectionManager(BaseObjectManager[_BaseListSectionT], Generic[_BaseListSectionT]):
    """Query and creation manager shared by all list-section types."""

    _ORDER_KEY = None

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _BaseListSectionT]"]:
        """Return the list-section retrieval API method."""
        return client.lists.section.get

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, _BaseListSectionT]"]:
        """Return the list-section creation API method."""
        return client.lists.section.add

    def _get_add_params(
            self,
            fields: JSONDict,
            *,
            add_params: Optional[JSONDict] = None,
    ) -> JSONDict:
        """Move section identifiers outside the Bitrix24 ``FIELDS`` mapping."""

        if "section_code" not in fields:
            raise ValueError("Pass section_code to add a list section.") from None

        endpoint_fields = ("section_code", "iblock_section_id")

        object_fields = {
            key: value
            for key, value in fields.items()
            if key not in endpoint_fields
        }

        params = super()._get_add_params(object_fields, add_params=add_params)

        for field_name in endpoint_fields:
            if field_name in fields:
                params[field_name] = fields[field_name]

        return params

    def filter(self, **filters: Any) -> Self:
        """Return sections filtered by SDK object attribute names."""
        return self._filter(**filters)

    def select(self, *fields: Text) -> Self:
        """Return sections with the requested SDK object fields selected."""
        return self._select(*fields)

    def select_all(self) -> Self:
        """Return sections with all registered fields requested."""
        return self._select_all()

    def add(
            self,
            *,
            section_code: Text,
            name: Text,
            iblock_section_id: int = MISSING,
            timeout: Timeout = None,
            **fields: Any,
    ) -> _BaseListSectionT:
        """Create a section in the manager's fixed Bitrix24 list."""

        fields: JSONDict = {
            **fields,
            "section_code": section_code,
            "name": name,
        }

        if iblock_section_id is not MISSING:
            fields["iblock_section_id"] = iblock_section_id

        return self._add(**fields, timeout=timeout)

    def add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[_BaseListSectionT]:
        """Create multiple sections through the client's batch API."""
        return self._add_many(objects_data, timeout=timeout)

    def update(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BitrixObjectBatchWriteResult[_BaseListSectionT]:
        """Update sections matching the current query in batches."""
        return self._update(**fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> BitrixObjectBatchWriteResult[_BaseListSectionT]:
        """Delete sections matching the current query through the batch API."""
        return self._delete(timeout=timeout)
