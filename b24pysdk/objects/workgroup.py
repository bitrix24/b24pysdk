from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Iterable, Optional, Text, TypeVar

from ..constants.group import GroupAvatarType, GroupPermissionRole, GroupPrivacy, GroupScrumTaskResponsible, GroupType
from ..errors import BitrixAPIError
from ..schemas.file import URLFile
from ..utils.case import camel_to_upper
from ..utils.types import JSONDict, Self
from ._base_object import BaseObject
from ._fields import BoolField, DateTimeField, DictField, EnumField, FileField, IntField, ObjectField, TextField
from ._managers import BaseObjectManager

if TYPE_CHECKING:
    from ..api.requests import BitrixAPIValuesRequest
    from ..client import ClientType
    from ..schemas.socialnetwork import WorkgroupListData
    from .department import Department  # noqa: F401
    from .user import User  # noqa: F401

__all__ = [
    "Workgroup",
    "WorkgroupManager",
]

_BITRIX_DATA_FIELD_ALIASES: Dict[Text, Text] = {
    "isPin": "IS_PIN",
    "pin": "IS_PIN",
    "privacyCode": "PRIVACY_CODE",
    "privacyType": "PRIVACY_CODE",
}


class Workgroup(BaseObject[int]):
    """Read-only Bitrix24 workgroup, project, scrum, or collaboration."""

    OBJECT_KEY = "workgroup"
    PK = int

    _IS_COMPLETE_WITHOUT_SELECT = False

    objects: "WorkgroupManager[Self]"

    bitrix_id = IntField("ID", is_pk=True)
    active = BoolField("ACTIVE", is_required=True)
    site_id = TextField("SITE_ID", is_required=True)
    subject_id = IntField("SUBJECT_ID", is_required=True)
    name = TextField("NAME", is_required=True)
    description = TextField("DESCRIPTION", is_required=True)
    keywords = TextField("KEYWORDS", is_required=True)
    closed = BoolField("CLOSED", is_required=True)
    visible = BoolField("VISIBLE", is_required=True)
    opened = BoolField("OPENED", is_required=True)
    date_create = TextField("DATE_CREATE", is_required=True)
    date_update = DateTimeField("DATE_UPDATE", is_required=True)
    date_activity = DateTimeField("DATE_ACTIVITY", is_required=True)
    image_id = IntField("IMAGE_ID", is_required=True)
    avatar_type = EnumField[GroupAvatarType]("AVATAR_TYPE", enum_class=GroupAvatarType)
    owner_id = IntField("OWNER_ID", is_required=True)
    owner = ObjectField["User"](owner_id, object_class="user")
    initiate_perms = EnumField[GroupPermissionRole]("INITIATE_PERMS", enum_class=GroupPermissionRole, is_required=True)
    number_of_members = IntField("NUMBER_OF_MEMBERS", is_required=True)
    number_of_moderators = IntField("NUMBER_OF_MODERATORS", is_required=True)
    project = BoolField("PROJECT", is_required=True)
    project_date_start = DateTimeField("PROJECT_DATE_START")
    project_date_finish = DateTimeField("PROJECT_DATE_FINISH")
    search_index = TextField("SEARCH_INDEX", is_required=True)
    landing = BoolField("LANDING", is_required=True)
    scrum_owner_id = IntField("SCRUM_OWNER_ID", is_required=True)
    scrum_owner = ObjectField["User"](scrum_owner_id, object_class="user")
    scrum_sprint_duration = IntField("SCRUM_SPRINT_DURATION", is_required=True)
    scrum_task_responsible = EnumField[GroupScrumTaskResponsible]("SCRUM_TASK_RESPONSIBLE", enum_class=GroupScrumTaskResponsible)
    workgroup_type = EnumField[GroupType]("TYPE", enum_class=GroupType, is_required=True)
    member_ids = IntField("MEMBERS", is_multiple=True, is_required=True)
    members = ObjectField["User"](member_ids, object_class="user")
    chat_id = IntField("CHAT_ID", is_required=True)
    dialog_id = TextField("DIALOG_ID", is_required=True)
    ordinary_member_ids = IntField("ORDINARY_MEMBERS", is_multiple=True, is_required=True)
    ordinary_members = ObjectField["User"](ordinary_member_ids, object_class="user")
    invited_member_ids = IntField("INVITED_MEMBERS", is_multiple=True, is_required=True)
    invited_members = ObjectField["User"](invited_member_ids, object_class="user")
    moderator_member_ids = IntField("MODERATOR_MEMBERS", is_multiple=True, is_required=True)
    moderator_members = ObjectField["User"](moderator_member_ids, object_class="user")
    site_ids = TextField("SITE_IDS", is_multiple=True, is_required=True)
    tags = TextField("TAGS", is_multiple=True)
    department_ids = IntField("DEPARTMENTS", is_multiple=True)
    departments = ObjectField["Department"](department_ids, object_class="department")
    number_of_members_plural = IntField("NUMBER_OF_MEMBERS_PLURAL", is_required=True)
    avatar = FileField[URLFile]("AVATAR", file_class=URLFile, is_read_only=True)
    avatar_types = DictField("AVATAR_TYPES")
    avatar_data = DictField("AVATAR_DATA")
    owner_data = DictField("OWNER_DATA")
    subject_data = DictField("SUBJECT_DATA")
    actions = DictField("ACTIONS")
    user_data = DictField("USER_DATA")
    is_pin = BoolField("IS_PIN", serialize_as=bool)
    privacy = EnumField[GroupPrivacy]("PRIVACY_CODE", enum_class=GroupPrivacy)
    list_of_members = DictField("LIST_OF_MEMBERS", is_multiple=True)
    features = DictField("FEATURES", is_multiple=True)
    list_of_members_awaiting_invite = DictField("LIST_OF_MEMBERS_AWAITING_INVITE", is_multiple=True)
    group_members_list = DictField("GROUP_MEMBERS_LIST", is_multiple=True)
    counters = DictField("COUNTERS")
    efficiency = IntField("EFFICIENCY")
    additional_data = DictField("ADDITIONAL_DATA")

    @classmethod
    def _normalize_bitrix_data(cls, bitrix_data: JSONDict, /) -> JSONDict:
        """Normalize workgroup responses to registered Bitrix24 field codes."""
        return {
            _BITRIX_DATA_FIELD_ALIASES.get(field_name, camel_to_upper(field_name)): value
            for field_name, value in bitrix_data.items()
        }

    def _get_bitrix_data(self) -> JSONDict:
        """Load complete workgroup data from Bitrix24."""
        try:
            return self.client.socialnetwork.api.workgroup.get(
                {
                    "groupId": self.bitrix_pk,
                    "select": self._meta.bitrix_codes,
                    "mode": "mobile",
                },
            ).result
        except BitrixAPIError as error:
            if error.error == "SONET_CONTROLLER_WORKGROUP_NOT_FOUND":
                raise self.DoesNotExist(
                    f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.",
                ) from error
            raise


_WorkgroupT = TypeVar("_WorkgroupT", bound=Workgroup)


class WorkgroupManager(BaseObjectManager[_WorkgroupT], Generic[_WorkgroupT]):
    """Query manager for Bitrix24 workgroups."""

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[WorkgroupListData, _WorkgroupT]"]:
        """Return the workgroup list API method."""
        return client.socialnetwork.api.workgroup.list

    def filter(self, **filters: Any) -> Self:
        """Return workgroups filtered by SDK object attribute names."""
        return self._filter(**filters)

    def from_pks(self, bitrix_pks: Iterable[int]) -> Self:
        """Return workgroups filtered by their Bitrix24 identifiers."""
        return self._from_pks(bitrix_pks)

    def order(self, *fields: Text) -> Self:
        """Return workgroups ordered by SDK object attribute names."""
        return self._order(*fields)

    def select(self, *fields: Text) -> Self:
        """Return workgroups with only the selected fields loaded eagerly."""
        return self._select(*fields)

    def select_all(self) -> Self:
        """Return workgroups with all registered fields requested."""
        return self._select_all()

    def start(self, start: Optional[int]) -> Self:
        """Return workgroups with a custom pagination start offset."""
        return self._start(start)

    def with_params(self, params: JSONDict) -> Self:
        """Return a query with ``socialnetwork.api.workgroup.list`` controls."""
        return self._with_params(params=params)


Workgroup.objects = WorkgroupManager()
