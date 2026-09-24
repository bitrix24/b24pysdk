from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Hashable,
    Iterable,
    List,
    Optional,
    Sequence,
    Text,
    Tuple,
    TypeVar,
    Union,
)
from urllib.parse import urljoin

from ...._constants import MISSING
from ....constants.list import ListIBlockType
from ....schemas.list.field import ListFieldListItem
from ....utils.converters import int_from_bitrix, text_from_bitrix
from ....utils.types import JSONDict, JSONList, Self, Timeout
from ..._base_object import BaseObject
from ..._fields import BoolField, DateTimeField, FileField, IntField, ObjectField, TextField
from ..._fields.base_field import BaseField
from ..._managers import BaseObjectManager
from ..._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult
from ...errors import BitrixObjectFieldError

if TYPE_CHECKING:
    from ....api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ....client import ClientType
    from ...user import User  # noqa: F401
    from ..field._base_list_field import BaseListField

__all__ = [
    "BaseListElement",
    "BaseListElementManager",
]


class BaseListElement(BaseObject[int]):
    """Shared object implementation for Bitrix24 list elements."""

    OBJECT_KEY = "list.element"
    PK = int

    _USERFIELD_BITRIX_CODE_PREFIX = "PROPERTY_"

    IBLOCK_TYPE_ID: ClassVar[Optional[ListIBlockType]] = None
    IBLOCK_ID: ClassVar[Optional[int]] = None

    objects: "BaseListElementManager[Self]"

    bitrix_id = IntField("ID", is_pk=True, request_name="element_id")
    code = TextField("CODE", is_required=True, is_updatable=False, request_name="element_code")
    name = TextField("NAME", is_required=True)
    iblock_section_id = IntField("IBLOCK_SECTION_ID")
    created_by_id = IntField("CREATED_BY", is_read_only=True)
    created_by = ObjectField["User"](created_by_id, object_class="user")
    created_user_name = TextField("CREATED_USER_NAME", is_read_only=True)
    active_to = DateTimeField("ACTIVE_TO")
    bp_published = BoolField("BP_PUBLISHED", is_read_only=True)
    date_create = DateTimeField("DATE_CREATE", is_read_only=True)
    preview_text = TextField("PREVIEW_TEXT")
    detail_text = TextField("DETAIL_TEXT")
    sort = IntField("SORT")
    preview_text_type = TextField("PREVIEW_TEXT_TYPE")
    detail_text_type = TextField("DETAIL_TEXT_TYPE")

    @classmethod
    def get_discriminator(cls) -> Tuple[Optional[ListIBlockType], Optional[int]]:
        """Return the list type and list identifier used by the registry."""
        return cls.IBLOCK_TYPE_ID, cls.IBLOCK_ID

    @classmethod
    def get_required_class_params(cls) -> JSONDict:
        """Return the list identifiers required by element API methods."""
        return {
            "iblock_type_id": cls.IBLOCK_TYPE_ID,
            "iblock_id": cls.IBLOCK_ID,
        }

    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> Dict[Text, "BaseListField"]:
        """Return list-field objects cached for this list discriminator."""

        cache_key = "list.field", self.get_discriminator()
        objects_cache = self.client.get_cache("bitrix_objects")
        fields = objects_cache.get(cache_key)

        if fields is None:
            field_objects = self.client.lists.field.get(**self._meta.required_class_params, timeout=timeout).values
            fields = {
                field_object.field_id: field_object
                for field_object in field_objects
            }
            objects_cache[cache_key] = fields

        return fields

    def get_field_title(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> Text:
        """Return the list-field title by Bitrix24 field code."""
        return self.get_field(bitrix_code, timeout=timeout).name

    def get_field_items(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> List[ListFieldListItem]:
        """Return selectable items for a list field."""

        display_values = self.get_field(bitrix_code, timeout=timeout).display_values_form

        if display_values is None:
            raise BitrixObjectFieldError(
                f"List field {bitrix_code!r} is not a selectable list field and has no items.",
            )

        items = []

        for bitrix_id, value in display_values.items():
            item_id = int_from_bitrix(bitrix_id, is_required=True)
            item_value = text_from_bitrix(value, is_required=True)
            items.append(ListFieldListItem(bitrix_id=item_id, value=item_value))

        return items

    def _get_bitrix_data(self) -> JSONDict:
        """Load complete element data from Bitrix24."""

        class_params = self._meta.required_class_params
        elements = self.client.lists.element.get(**class_params, element_id=self.bitrix_pk).result

        if not elements:
            message = f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist."
            raise self.DoesNotExist(message)

        if len(elements) > 1:
            message = f"Multiple {self.__class__.__name__} objects returned for pk={self.bitrix_pk!r}."
            raise self.MultipleObjectsReturned(message)

        return elements[0]

    def get_field_value(
            self,
            bitrix_code: Text,
            *,
            bitrix_field: Optional[BaseField[Any, Any]] = None,
    ) -> Any:
        """Return a list-property value without its property-value identifiers.

        ``lists.element.get`` wraps every ``PROPERTY_*`` value in a mapping
        whose keys are property-value IDs. Ordinary descriptors consume only
        the mapping values. ``FileField`` keeps each one-item mapping because a
        list file needs both the property-value ID and the file ID.
        """

        if not bitrix_code.startswith("PROPERTY_"):
            return super().get_field_value(bitrix_code, bitrix_field=bitrix_field)

        if bitrix_field is None:
            bitrix_field = self._meta.get_field_by_bitrix_code(bitrix_code)

        local_data = self._local_data
        has_local_value = local_data is not None and bitrix_code in local_data
        value = super().get_field_value(bitrix_code, bitrix_field=bitrix_field)

        if has_local_value or not isinstance(value, Mapping):
            return value

        if isinstance(bitrix_field, FileField):
            values = [{property_value_id: file_id} for property_value_id, file_id in value.items()]
        else:
            values = list(value.values())

        if bitrix_field.is_multiple:
            return values

        if not values:
            return None

        if len(values) > 1:
            message = f"Single field {bitrix_code!r} returned multiple Bitrix24 property values."
            raise ValueError(message)

        return values[0]

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the list-element update API method."""
        return client.lists.element.update

    def _get_update_params(self, updated_data: JSONDict) -> JSONDict:
        """Build a full element payload while leaving existing files untouched."""

        bitrix_data = self._bitrix_data

        if bitrix_data is None or not self._is_bitrix_data_fully_loaded:
            bitrix_data = self._reload_bitrix_data()

        fields: JSONDict = {}

        for bitrix_code, raw_value in bitrix_data.items():
            if raw_value is None and bitrix_code not in updated_data:
                continue

            bitrix_field = self._meta.fields_by_bitrix_code.get(bitrix_code)

            if bitrix_code.startswith("PROPERTY_") and bitrix_field is None:
                message = (
                    f"Declare list property {bitrix_code!r} on {self.__class__.__name__} "
                    "before updating an element so its current value is not cleared."
                )
                raise BitrixObjectFieldError(message)

            is_not_writable = (
                bitrix_field is None
                or bitrix_field.is_pk
                or bitrix_field.is_read_only
                or not bitrix_field.is_updatable
            )

            if is_not_writable:
                continue

            if isinstance(bitrix_field, FileField):
                continue

            if bitrix_code.startswith("PROPERTY_") and isinstance(raw_value, Mapping):
                fields[bitrix_code] = self.get_field_value(bitrix_code, bitrix_field=bitrix_field)
            else:
                fields[bitrix_code] = raw_value

        fields.update(updated_data)

        return super()._get_update_params(fields)

    def update(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> bool:
        """Update this element without clearing omitted ordinary fields."""
        return self._update(**fields, timeout=timeout)

    def save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save local changes without clearing omitted ordinary fields."""
        return self._save(update_fields=update_fields, timeout=timeout)

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the list-element delete API method."""
        return client.lists.element.delete

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Delete this element from Bitrix24."""
        return self._delete(timeout=timeout)

    def get_file_urls(
            self,
            field_id: int,
            *,
            timeout: Timeout = None,
    ) -> List[Text]:
        """Return absolute download URLs for one file property."""

        urls = self.client.lists.element.get.file.url(
            **self._meta.required_class_params,
            element_id=self.bitrix_pk,
            field_id=field_id,
            timeout=timeout,
        ).result

        base_url = f"{self._base_url}/"
        return [urljoin(base_url, url) for url in urls]


_BaseListElementT = TypeVar("_BaseListElementT", bound=BaseListElement)


class BaseListElementManager(BaseObjectManager[_BaseListElementT], Generic[_BaseListElementT]):
    """Query and creation manager shared by all list-element types."""

    _ORDER_KEY = None

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _BaseListElementT]"]:
        """Return the list-element retrieval API method."""
        return client.lists.element.get

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, _BaseListElementT]"]:
        """Return the list-element creation API method."""
        return client.lists.element.add

    def _get_add_params(
            self,
            fields: JSONDict,
            *,
            add_params: Optional[JSONDict] = None,
    ) -> JSONDict:
        """Move endpoint-specific element parameters outside ``FIELDS``."""

        if "element_code" not in fields:
            raise ValueError("Pass element_code to add a list element.") from None

        endpoint_fields = ("element_code", "iblock_section_id", "list_element_url")

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
        """Return elements filtered by SDK object attribute names."""
        return self._filter(**filters)

    def from_pks(self, bitrix_pks: Iterable[int]) -> Self:
        """Return elements whose identifiers belong to the supplied iterable."""
        return self._from_pks(bitrix_pks)

    def select(self, *fields: Text) -> Self:
        """Return elements with the requested SDK object fields selected."""
        return self._select(*fields)

    def select_all(self) -> Self:
        """Return elements with all registered fields requested."""
        return self._select_all()

    def start(self, start: Optional[int]) -> Self:
        """Return elements with a custom pagination start offset."""
        return self._start(start)

    def add(
            self,
            *,
            element_code: Text,
            name: Text,
            iblock_section_id: int = MISSING,
            list_element_url: Text = MISSING,
            timeout: Timeout = None,
            **fields: Any,
    ) -> _BaseListElementT:
        """Create an element in the manager's fixed Bitrix24 list."""

        fields: JSONDict = {
            **fields,
            "element_code": element_code,
            "name": name,
        }

        if iblock_section_id is not MISSING:
            fields["iblock_section_id"] = iblock_section_id

        if list_element_url is not MISSING:
            fields["list_element_url"] = list_element_url

        return self._add(**fields, timeout=timeout)

    def add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[_BaseListElementT]:
        """Create multiple elements through the client's batch API."""
        return self._add_many(objects_data, timeout=timeout)

    def update(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BitrixObjectBatchWriteResult[_BaseListElementT]:
        """Update matching elements without clearing omitted ordinary fields."""
        return self._update(**fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> BitrixObjectBatchWriteResult[_BaseListElementT]:
        """Delete matching elements through the client's batch API."""
        return self._delete(timeout=timeout)
