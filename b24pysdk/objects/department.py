from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Hashable, Iterable, Mapping, Optional, Sequence, Text, TypeVar, Union

from .._constants import MISSING
from ..utils.types import JSONDict, JSONList, Self, Timeout
from ._base_object import BaseObject
from ._fields import IntField, ObjectField, TextField
from ._managers import BaseFieldManager, BaseObjectManager
from ._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult
from .errors import BitrixObjectError

if TYPE_CHECKING:
    from ..api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ..client import ClientType
    from .user import User

__all__ = [
    "Department",
    "DepartmentFieldManager",
    "DepartmentManager",
]


class Department(BaseObject[int]):
    """Bitrix24 company department."""

    _OBJECT_KEY = "department"
    _PK_TYPE = int
    _UPDATE_KEY = None

    fields: "DepartmentFieldManager[Self]"
    objects: "DepartmentManager[Self]"

    bitrix_id = IntField("ID", is_pk=True)
    name = TextField("NAME", is_required=True)
    sort = IntField("SORT", is_required=True)
    parent_id = IntField("PARENT", is_missing_allowed=True)
    parent: Optional[Self] = ObjectField(parent_id, object_class="department")
    uf_head_id = IntField("UF_HEAD", is_missing_allowed=True)
    uf_head: Optional["User"] = ObjectField(uf_head_id, object_class="user")

    def _get_bitrix_data(self) -> JSONDict:
        """Load raw department data from Bitrix24."""

        result = self.client.department.get(bitrix_id=self.bitrix_pk).result

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
            name: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            parent_id: Optional[int] = MISSING,
            parent: Optional[Self] = MISSING,
            head_id: Optional[int] = MISSING,
            uf_head: Optional["User"] = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Update this department in Bitrix24."""

        if parent_id is not MISSING and parent is not MISSING:
            raise ValueError("Pass either parent_id or parent, not both.")

        if head_id is not MISSING and uf_head is not MISSING:
            raise ValueError("Pass either head_id or uf_head, not both.")

        fields: JSONDict = {}

        if name is not MISSING:
            fields["name"] = name

        if sort is not MISSING:
            fields["sort"] = sort

        if parent_id is not MISSING:
            fields["parent_id"] = parent_id

        if parent is not MISSING:
            fields["parent"] = parent

        if head_id is not MISSING:
            fields["uf_head_id"] = head_id

        if uf_head is not MISSING:
            fields["uf_head"] = uf_head

        return self._update(**fields, timeout=timeout)

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the update API method resolved from the supplied client."""
        return client.department.update

    def save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save local changes or selected current department fields to Bitrix24."""
        return self._save(update_fields=update_fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Delete this department from Bitrix24."""
        return self._delete(timeout=timeout)

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the delete API method resolved from the supplied client."""
        return client.department.delete


_DepartmentT = TypeVar("_DepartmentT", bound=Department)


class DepartmentFieldManager(BaseFieldManager[_DepartmentT], Generic[_DepartmentT]):
    """Field metadata manager for Bitrix24 departments."""

    __slots__ = ()

    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> Dict[Text, Text]:
        """Return all Bitrix24 department field metadata."""
        return self._client.department.fields(timeout=timeout).result


class DepartmentManager(BaseObjectManager[_DepartmentT], Generic[_DepartmentT]):
    """Query manager for Bitrix24 departments."""

    _ADD_KEY = None
    _FILTER_KEY = None
    _ORDER_KEY = None

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _DepartmentT]"]:
        """Return the load API method resolved from the supplied client."""
        return client.department.get

    def filter(self, **filters: Any) -> Self:
        """Return departments filtered by SDK object attribute names."""
        return self._filter(**filters)

    def order(self, *fields: Text) -> Self:
        """Return departments ordered by SDK object attribute names."""
        return self._order(*fields)

    def _add_order_param(self, params: JSONDict):
        """Add ``department.get`` ordering parameters to request parameters."""

        if self._is_fast:
            return

        order_param = self._get_order_param()

        if order_param is None:
            return

        if len(order_param) != 1:
            raise BitrixObjectError("department.get supports ordering only by one field.")

        sort, order = next(iter(order_param.items()))

        params["sort"] = sort
        params["order"] = order

    def start(self, start: Optional[int]) -> Self:
        """Return departments with a custom Bitrix24 pagination start offset."""
        return self._start(start)

    def add(
            self,
            *,
            name: Text,
            parent_id: Optional[int] = MISSING,
            parent: Optional[_DepartmentT] = MISSING,
            sort: Optional[int] = MISSING,
            head_id: Optional[int] = MISSING,
            uf_head: Optional["User"] = MISSING,
            timeout: Timeout = None,
    ) -> _DepartmentT:
        """Create a Bitrix24 department."""

        if parent_id is MISSING and parent is MISSING:
            raise ValueError("Pass either parent_id or parent.")

        if parent_id is not MISSING and parent is not MISSING:
            raise ValueError("Pass either parent_id or parent, not both.")

        if head_id is not MISSING and uf_head is not MISSING:
            raise ValueError("Pass either head_id or uf_head, not both.")

        fields: JSONDict = {
            "name": name,
        }

        if parent_id is not MISSING:
            fields["parent_id"] = parent_id

        if parent is not MISSING:
            fields["parent"] = parent

        if sort is not MISSING:
            fields["sort"] = sort

        if head_id is not MISSING:
            fields["uf_head_id"] = head_id

        if uf_head is not MISSING:
            fields["uf_head"] = uf_head

        return self._add(**fields, timeout=timeout)

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, _DepartmentT]"]:
        """Return the add API method resolved from the supplied client."""
        return client.department.add

    def add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[_DepartmentT]:
        """Create many Bitrix24 departments from SDK field dictionaries."""
        return self._add_many(objects_data, timeout=timeout)

    def update(
            self,
            *,
            name: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            parent_id: Optional[int] = MISSING,
            parent: Optional[_DepartmentT] = MISSING,
            head_id: Optional[int] = MISSING,
            uf_head: Optional["User"] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResult[_DepartmentT]:
        """Update departments matching the current query in batches."""

        if parent_id is not MISSING and parent is not MISSING:
            raise ValueError("Pass either parent_id or parent, not both.")

        if head_id is not MISSING and uf_head is not MISSING:
            raise ValueError("Pass either head_id or uf_head, not both.")

        fields: JSONDict = {}

        if name is not MISSING:
            fields["name"] = name

        if sort is not MISSING:
            fields["sort"] = sort

        if parent_id is not MISSING:
            fields["parent_id"] = parent_id

        if parent is not MISSING:
            fields["parent"] = parent

        if head_id is not MISSING:
            fields["uf_head_id"] = head_id

        if uf_head is not MISSING:
            fields["uf_head"] = uf_head

        return self._update(**fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> BitrixObjectBatchWriteResult[_DepartmentT]:
        """Delete departments matching the current query in batches."""
        return self._delete(timeout=timeout)


Department.fields = DepartmentFieldManager()
Department.objects = DepartmentManager()
