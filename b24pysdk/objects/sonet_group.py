from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Any, Callable, ClassVar, FrozenSet, Generic, Hashable, Iterable, List, Literal, Mapping, Optional, Sequence, Text, TypeVar, Union

from .._constants import MISSING
from ..constants.group import GroupPermissionRole, GroupPermissionRoleLiteral
from ..schemas.file import URLFile
from ..schemas.sonet_group.user import SonetGroupMember
from ..utils.types import JSONDict, JSONList, Self, Timeout
from ._base_object import BaseObject
from ._fields import BoolField, DateTimeField, EnumField, FileField, IntField, ObjectField, TextField
from ._filter_lookups import FilterLookup
from ._managers import BaseObjectManager
from ._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult

if TYPE_CHECKING:
    from ..api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ..client import ClientType
    from .user import User

__all__ = [
    "SonetGroup",
    "SonetGroupManager",
]


class SonetGroup(BaseObject[int]):
    """Bitrix24 social-network workgroup or project."""

    OBJECT_KEY = "sonet_group"
    PK = int

    _UPDATE_KEY = None
    _FILTER_LOOKUPS: ClassVar[FrozenSet[FilterLookup]] = frozenset({
        FilterLookup.NOT_EXACT,
        FilterLookup.GT,
        FilterLookup.GTE,
        FilterLookup.CONTAINS,
    })

    objects: "SonetGroupManager[Self]"

    bitrix_id = IntField("ID", is_pk=True)
    name = TextField("NAME", is_required=True)
    description = TextField("DESCRIPTION")
    date_create = DateTimeField("DATE_CREATE", is_required=True, is_read_only=True)
    date_update = DateTimeField("DATE_UPDATE", is_required=True, is_read_only=True)
    date_activity = DateTimeField("DATE_ACTIVITY", is_required=True, is_read_only=True)
    active = BoolField("ACTIVE", is_required=True, is_read_only=True)
    visible = BoolField("VISIBLE", is_required=True)
    opened = BoolField("OPENED", is_required=True)
    closed = BoolField("CLOSED", is_required=True)
    subject_id = IntField("SUBJECT_ID", is_required=True, is_updatable=False)
    owner_id = IntField("OWNER_ID", is_required=True)
    owner = ObjectField["User"](owner_id, object_class="user")
    keywords = TextField("KEYWORDS")
    number_of_members = IntField("NUMBER_OF_MEMBERS", is_required=True, is_read_only=True)
    subject_name = TextField("SUBJECT_NAME", is_required=True, is_read_only=True)
    project = BoolField("PROJECT", is_required=True, is_updatable=False)
    is_extranet = BoolField("IS_EXTRANET", is_required=True, is_read_only=True)
    initiate_perms = EnumField[GroupPermissionRole]("INITIATE_PERMS", enum_class=GroupPermissionRole)
    project_date_start = DateTimeField("PROJECT_DATE_START")
    project_date_finish = DateTimeField("PROJECT_DATE_FINISH")
    scrum_master_id = IntField("SCRUM_MASTER_ID", is_updatable=False)
    image = FileField[URLFile]("IMAGE", file_class=URLFile)
    image_file_id = IntField("IMAGE_FILE_ID")

    def _get_bitrix_data(self) -> JSONDict:
        """Load complete group data from Bitrix24."""

        sonet_groups = self.client.sonet_group.get(filter={"ID": self.bitrix_pk}).result

        if not sonet_groups:
            raise self.DoesNotExist(
                f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.",
            )

        if len(sonet_groups) > 1:
            raise self.MultipleObjectsReturned(
                f"Multiple {self.__class__.__name__} objects returned "
                f"for pk={self.bitrix_pk!r}.",
            )

        return sonet_groups[0]

    def update(  # noqa: C901, PLR0912
            self,
            *,
            name: Text = MISSING,
            description: Text = MISSING,
            visible: bool = MISSING,
            opened: bool = MISSING,
            closed: bool = MISSING,
            keywords: Text = MISSING,
            initiate_perms: Annotated[Text, GroupPermissionRoleLiteral] = MISSING,
            project_date_start: datetime = MISSING,
            project_date_finish: datetime = MISSING,
            owner_id: int = MISSING,
            owner: "User" = MISSING,
            image: URLFile = MISSING,
            image_file_id: int = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Update this group in Bitrix24."""

        if owner_id is not MISSING and owner is not MISSING:
            raise ValueError("Pass either owner_id or owner, not both.")

        fields: JSONDict = {}

        if name is not MISSING:
            fields["name"] = name

        if description is not MISSING:
            fields["description"] = description

        if visible is not MISSING:
            fields["visible"] = visible

        if opened is not MISSING:
            fields["opened"] = opened

        if closed is not MISSING:
            fields["closed"] = closed

        if keywords is not MISSING:
            fields["keywords"] = keywords

        if initiate_perms is not MISSING:
            fields["initiate_perms"] = initiate_perms

        if project_date_start is not MISSING:
            fields["project_date_start"] = project_date_start

        if project_date_finish is not MISSING:
            fields["project_date_finish"] = project_date_finish

        if owner_id is not MISSING:
            fields["owner_id"] = owner_id

        if owner is not MISSING:
            fields["owner"] = owner

        if image is not MISSING:
            fields["image"] = image

        if image_file_id is not MISSING:
            fields["image_file_id"] = image_file_id

        return self._update(**fields, timeout=timeout)

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the update method under the object's boolean contract."""
        return client.sonet_group.update

    def save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save local changes or selected current group fields to Bitrix24."""
        return self._save(update_fields=update_fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> bool:
        """Delete this group from Bitrix24."""
        return self._delete(timeout=timeout)

    def _get_delete_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the group deletion API method."""
        return client.sonet_group.delete

    def set_owner(
            self,
            user_id: int,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Assign a new owner and synchronize the loaded owner identifier."""

        result = self.client.sonet_group.setowner(
            self.bitrix_pk,
            user_id,
            timeout=timeout,
        ).result

        if result:
            self._apply_updated_data({
                "OWNER_ID": self.__class__.owner_id.to_bitrix_value(user_id),
            })

        return result

    def invite_users(
            self,
            user_id: Union[int, Iterable[int]],
            *,
            message: Text = MISSING,
            timeout: Timeout = None,
    ) -> List[int]:
        """Invite one or more users to this group."""

        result = self.client.sonet_group.user.invite(
            group_id=self.bitrix_pk,
            user_id=user_id,
            message=message,
            timeout=timeout,
        ).result

        return [int(user_id) for user_id in result]

    def request_join(
            self,
            *,
            message: Text = MISSING,
            timeout: Timeout = None,
    ) -> bool:
        """Request membership in this group for the current user."""
        return self.client.sonet_group.user.request(
            group_id=self.bitrix_pk,
            message=message,
            timeout=timeout,
        ).result

    def add_users(
            self,
            user_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> List[int]:
        """Add one or more users to this group without confirmation."""

        result = self.client.sonet_group.user.add(
            group_id=self.bitrix_pk,
            user_id=user_id,
            timeout=timeout,
        ).result

        return [int(user_id) for user_id in result]

    def update_users_role(
            self,
            user_id: Union[int, Iterable[int]],
            role: Annotated[Text, Literal["E", "K"]],
            *,
            timeout: Timeout = None,
    ) -> List[int]:
        """Change the role of one or more participants in this group."""

        result = self.client.sonet_group.user.update(
            group_id=self.bitrix_pk,
            user_id=user_id,
            role=role,
            timeout=timeout,
        ).result

        return [int(user_id) for user_id in result]

    def get_members(self, *, timeout: Timeout = None) -> List[SonetGroupMember]:
        """Return active participants in this group."""
        return self.client.sonet_group.user.get(self.bitrix_pk, timeout=timeout).values

    def remove_users(
            self,
            user_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> List[int]:
        """Remove one or more participants from this group."""

        result = self.client.sonet_group.user.delete(
            group_id=self.bitrix_pk,
            user_id=user_id,
            timeout=timeout,
        ).result

        return [int(user_id) for user_id in result]

    def feature_access(
            self,
            feature: Text,
            operation: Text,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Check whether the current user can perform an operation in a group feature."""
        return self.client.sonet_group.feature.access(
            group_id=self.bitrix_pk,
            feature=feature,
            operation=operation,
            timeout=timeout,
        ).result


_SonetGroupT = TypeVar("_SonetGroupT", bound=SonetGroup)


class SonetGroupManager(BaseObjectManager[_SonetGroupT], Generic[_SonetGroupT]):
    """Query and creation manager for Bitrix24 social-network groups."""

    _ADD_KEY = None

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _SonetGroupT]"]:
        """Return the group list API method."""
        return client.sonet_group.get

    def filter(self, **filters: Any) -> Self:
        """Return groups filtered by SDK object attribute names."""
        return self._filter(**filters)

    def order(self, *fields: Text) -> Self:
        """Return groups ordered by SDK object attribute names."""
        return self._order(*fields)

    def start(self, start: Optional[int]) -> Self:
        """Return groups with a custom pagination start offset."""
        return self._start(start)

    def with_admin_mode(self, admin_mode: bool = True) -> Self:
        """Return groups query with permission checks enabled or disabled."""
        return self._with_params(is_admin=admin_mode)

    def add(  # noqa: C901, PLR0912
            self,
            *,
            name: Text,
            description: Text = MISSING,
            visible: bool = MISSING,
            opened: bool = MISSING,
            closed: bool = MISSING,
            keywords: Text = MISSING,
            initiate_perms: Annotated[Text, GroupPermissionRoleLiteral] = MISSING,
            project: bool = MISSING,
            project_date_start: datetime = MISSING,
            project_date_finish: datetime = MISSING,
            scrum_master_id: int = MISSING,
            owner_id: int = MISSING,
            owner: "User" = MISSING,
            image: URLFile = MISSING,
            image_file_id: int = MISSING,
            site_ids: Iterable[Text] = MISSING,
            subject_id: int = MISSING,
            timeout: Timeout = None,
    ) -> _SonetGroupT:
        """Create a Bitrix24 social-network group or project."""

        if owner_id is not MISSING and owner is not MISSING:
            raise ValueError("Pass either owner_id or owner, not both.")

        fields: JSONDict = {
            "name": name,
        }

        if description is not MISSING:
            fields["description"] = description

        if visible is not MISSING:
            fields["visible"] = visible

        if opened is not MISSING:
            fields["opened"] = opened

        if closed is not MISSING:
            fields["closed"] = closed

        if keywords is not MISSING:
            fields["keywords"] = keywords

        if initiate_perms is not MISSING:
            fields["initiate_perms"] = initiate_perms

        if project is not MISSING:
            fields["project"] = project

        if project_date_start is not MISSING:
            fields["project_date_start"] = project_date_start

        if project_date_finish is not MISSING:
            fields["project_date_finish"] = project_date_finish

        if scrum_master_id is not MISSING:
            fields["scrum_master_id"] = scrum_master_id

        if owner_id is not MISSING:
            fields["owner_id"] = owner_id

        if owner is not MISSING:
            fields["owner"] = owner

        if image is not MISSING:
            fields["image"] = image

        if image_file_id is not MISSING:
            fields["image_file_id"] = image_file_id

        if subject_id is not MISSING:
            fields["subject_id"] = subject_id

        add_params: JSONDict = {}

        if site_ids is not MISSING:
            add_params["site_id"] = site_ids

        return self._add(add_params or None, timeout=timeout, **fields)

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, _SonetGroupT]"]:
        """Return the group creation API method."""
        return client.sonet_group.create

    def add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[_SonetGroupT]:
        """Create multiple groups from SDK field dictionaries."""
        return self._add_many(objects_data, timeout=timeout)

    def update(  # noqa: C901, PLR0912
            self,
            *,
            name: Text = MISSING,
            description: Text = MISSING,
            visible: bool = MISSING,
            opened: bool = MISSING,
            closed: bool = MISSING,
            keywords: Text = MISSING,
            initiate_perms: Annotated[Text, GroupPermissionRoleLiteral] = MISSING,
            project_date_start: datetime = MISSING,
            project_date_finish: datetime = MISSING,
            owner_id: int = MISSING,
            owner: "User" = MISSING,
            image: URLFile = MISSING,
            image_file_id: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchWriteResult[_SonetGroupT]:
        """Update groups matching the current query in batches."""

        if owner_id is not MISSING and owner is not MISSING:
            raise ValueError("Pass either owner_id or owner, not both.")

        fields: JSONDict = {}

        if name is not MISSING:
            fields["name"] = name

        if description is not MISSING:
            fields["description"] = description

        if visible is not MISSING:
            fields["visible"] = visible

        if opened is not MISSING:
            fields["opened"] = opened

        if closed is not MISSING:
            fields["closed"] = closed

        if keywords is not MISSING:
            fields["keywords"] = keywords

        if initiate_perms is not MISSING:
            fields["initiate_perms"] = initiate_perms

        if project_date_start is not MISSING:
            fields["project_date_start"] = project_date_start

        if project_date_finish is not MISSING:
            fields["project_date_finish"] = project_date_finish

        if owner_id is not MISSING:
            fields["owner_id"] = owner_id

        if owner is not MISSING:
            fields["owner"] = owner

        if image is not MISSING:
            fields["image"] = image

        if image_file_id is not MISSING:
            fields["image_file_id"] = image_file_id

        return self._update(**fields, timeout=timeout)

    def delete(self, *, timeout: Timeout = None) -> BitrixObjectBatchWriteResult[_SonetGroupT]:
        """Delete groups matching the current query in batches."""
        return self._delete(timeout=timeout)


SonetGroup.objects = SonetGroupManager()
