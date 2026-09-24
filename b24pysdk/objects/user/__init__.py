from typing import TYPE_CHECKING, Annotated, Any, Callable, Dict, Generic, Hashable, Iterable, List, Literal, Mapping, Optional, Sequence, Text, TypeVar, Union

from ..._constants import MISSING
from ...constants.user import PersonalGender, UserType
from ...schemas.file import URLFile
from ...schemas.user.userfield import UserUserfieldListItem
from ...utils.types import JSONDict, JSONList, Self, Timeout
from .._base_object import BaseObject
from .._fields import BoolField, DateField, DateTimeField, EnumField, FileField, IntField, ObjectField, TextField, TimeZoneField
from .._managers import BaseFieldManager, BaseObjectManager
from .._object_results import BitrixObjectBatchAddResult, BitrixObjectBatchWriteResult
from ..errors import BitrixObjectFieldError

if TYPE_CHECKING:
    from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ...client import ClientType
    from ..department import Department  # noqa: F401
    from .userfield import UserUserfield

__all__ = [
    "User",
    "UserFieldManager",
    "UserManager",
]


class User(BaseObject[int]):
    """Bitrix24 portal user."""

    OBJECT_KEY = "user"
    PK = int

    _UPDATE_KEY = None
    _USERFIELD_BITRIX_CODE_PREFIX = "UF_USR_"

    fields: "UserFieldManager[Self]"
    objects: "UserManager[Self]"

    bitrix_id = IntField("ID", is_pk=True)
    xml_id = TextField("XML_ID")
    active = BoolField("ACTIVE", is_required=True)
    name = TextField("NAME")
    last_name = TextField("LAST_NAME")
    second_name = TextField("SECOND_NAME")
    title = TextField("TITLE")
    email = TextField("EMAIL")
    last_login = DateTimeField("LAST_LOGIN", is_read_only=True)
    date_register = DateTimeField("DATE_REGISTER", is_required=True, is_read_only=True)
    time_zone = TimeZoneField("TIME_ZONE")
    is_online = BoolField("IS_ONLINE", is_required=True, is_read_only=True)
    timestamp_x = DateTimeField("TIMESTAMP_X", is_read_only=True)
    last_activity_date = DateTimeField("LAST_ACTIVITY_DATE", is_read_only=True)
    personal_gender = EnumField[PersonalGender]("PERSONAL_GENDER", enum_class=PersonalGender)
    personal_www = TextField("PERSONAL_WWW")
    personal_birthday = DateField("PERSONAL_BIRTHDAY")
    personal_photo = FileField[URLFile]("PERSONAL_PHOTO", file_class=URLFile)
    personal_icq = TextField("PERSONAL_ICQ")
    personal_phone = TextField("PERSONAL_PHONE")
    personal_fax = TextField("PERSONAL_FAX")
    personal_profession = TextField("PERSONAL_PROFESSION")
    personal_mobile = TextField("PERSONAL_MOBILE")
    personal_pager = TextField("PERSONAL_PAGER")
    personal_street = TextField("PERSONAL_STREET")
    personal_city = TextField("PERSONAL_CITY")
    personal_state = TextField("PERSONAL_STATE")
    personal_zip = TextField("PERSONAL_ZIP")
    personal_country = TextField("PERSONAL_COUNTRY")
    personal_mailbox = TextField("PERSONAL_MAILBOX")
    personal_notes = TextField("PERSONAL_NOTES")
    work_phone = TextField("WORK_PHONE")
    work_company = TextField("WORK_COMPANY")
    work_position = TextField("WORK_POSITION")
    work_department = TextField("WORK_DEPARTMENT")
    work_www = TextField("WORK_WWW")
    work_fax = TextField("WORK_FAX")
    work_pager = TextField("WORK_PAGER")
    work_street = TextField("WORK_STREET")
    work_mailbox = TextField("WORK_MAILBOX")
    work_city = TextField("WORK_CITY")
    work_state = TextField("WORK_STATE")
    work_zip = TextField("WORK_ZIP")
    work_country = TextField("WORK_COUNTRY")
    work_profile = TextField("WORK_PROFILE")
    # work_logo = TextField("WORK_LOGO")
    work_notes = TextField("WORK_NOTES")
    uf_skype_link = TextField("UF_SKYPE_LINK")
    uf_zoom = TextField("UF_ZOOM")
    uf_employment_date = DateField("UF_EMPLOYMENT_DATE")
    uf_timeman = TextField("UF_TIMEMAN")
    uf_department_ids = IntField("UF_DEPARTMENT", is_multiple=True)
    uf_departments = ObjectField["Department"](uf_department_ids, object_class="department")
    uf_interests = TextField("UF_INTERESTS")
    uf_skills = TextField("UF_SKILLS")
    uf_web_sites = TextField("UF_WEB_SITES")
    uf_xing = TextField("UF_XING")
    uf_linkedin = TextField("UF_LINKEDIN")
    uf_facebook = TextField("UF_FACEBOOK")
    uf_twitter = TextField("UF_TWITTER")
    uf_skype = TextField("UF_SKYPE")
    uf_district = TextField("UF_DISTRICT")
    uf_phone_inner = TextField("UF_PHONE_INNER")
    user_type = EnumField[UserType]("USER_TYPE", enum_class=UserType, is_required=True)

    @property
    def url(self) -> Text:
        """Return the absolute Bitrix24 user profile URL."""
        return f"{self._base_url}/company/personal/user/{self.bitrix_pk}/"

    def _get_userfields(
            self,
            *,
            timeout: Timeout = None,
    ) -> Dict[Text, "UserUserfield"]:
        """Return all user custom-field objects cached for this client."""

        cache_key = "user.userfield", None
        objects_cache = self.client.get_cache("bitrix_objects")
        userfields = objects_cache.get(cache_key)

        if userfields is None:
            userfield_objects = self.client.user.userfield.list(timeout=timeout).values
            userfields = {
                userfield_object.field_name: userfield_object
                for userfield_object in userfield_objects
            }
            objects_cache[cache_key] = userfields

        return userfields

    def _get_userfield(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> "UserUserfield":
        """Return cached metadata for one user custom field."""
        try:
            return self._get_userfields(timeout=timeout)[bitrix_code]
        except KeyError:
            raise BitrixObjectFieldError(
                f"{self.__class__.__name__} has no user custom field metadata for {bitrix_code!r}.",
            ) from None

    def get_field(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> Any:
        """Return field metadata by Bitrix24 field code."""

        userfield_bitrix_code_prefix = self._USERFIELD_BITRIX_CODE_PREFIX

        if (
                userfield_bitrix_code_prefix is not None
                and bitrix_code.startswith(userfield_bitrix_code_prefix)
        ):
            return self._get_userfield(bitrix_code, timeout=timeout)

        return super().get_field(bitrix_code, timeout=timeout)

    def get_field_title(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> Text:
        """Return the localized user field title by Bitrix24 field code.

        ``user.fields`` contains titles for both standard and custom user
        fields. Calling the base metadata lookup deliberately bypasses
        ``User.get_field()``, which returns a ``UserUserfield`` object for a
        custom field so its selectable items remain available.
        """
        return super().get_field(bitrix_code, timeout=timeout)

    def get_field_items(
            self,
            bitrix_code: Text,
            *,
            timeout: Timeout = None,
    ) -> List[UserUserfieldListItem]:
        """Return selectable items for a user custom list field."""

        userfield_bitrix_code_prefix = self._USERFIELD_BITRIX_CODE_PREFIX

        if (
                userfield_bitrix_code_prefix is None
                or not bitrix_code.startswith(userfield_bitrix_code_prefix)
        ):
            raise BitrixObjectFieldError(
                f"User field {bitrix_code!r} is not a user custom field and has no selectable items.",
            )

        userfield_object = self._get_userfield(bitrix_code, timeout=timeout)
        items = userfield_object.list

        if items is None:
            raise BitrixObjectFieldError(
                f"User custom field {bitrix_code!r} is not a list field and has no selectable items.",
            )

        if not isinstance(items, list):
            raise BitrixObjectFieldError(
                f"User custom field {bitrix_code!r} returned invalid selectable items metadata.",
            )

        return items

    def _get_bitrix_data(self) -> JSONDict:
        """Load raw user data from Bitrix24."""

        result = self.client.user.get(filter={"ID": self.bitrix_pk}, admin_mode=True).result

        if not result:
            raise self.DoesNotExist(f"{self.__class__.__name__} with pk={self.bitrix_pk!r} does not exist.")

        if len(result) > 1:
            raise self.MultipleObjectsReturned(
                f"Multiple {self.__class__.__name__} objects returned for pk={self.bitrix_pk!r}.",
            )

        return result[0]

    def update(self, *, timeout: Timeout = None, **fields: Any) -> bool:
        """Update this user in Bitrix24."""
        return self._update(**fields, timeout=timeout)

    def _get_update_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIRequest[bool]"]:
        """Return the update API method resolved from the supplied client."""
        return client.user.update

    def save(
            self,
            update_fields: Optional[Iterable[Text]] = None,
            *,
            timeout: Timeout = None,
    ) -> bool:
        """Save local changes or selected current user fields to Bitrix24."""
        return self._save(update_fields=update_fields, timeout=timeout)


_UserT = TypeVar("_UserT", bound=User)


class UserFieldManager(BaseFieldManager[_UserT], Generic[_UserT]):
    """Field metadata manager for Bitrix24 users."""

    __slots__ = ()

    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> JSONDict:
        """Return all Bitrix24 user field metadata."""
        return self._client.user.fields(timeout=timeout).result


class UserManager(BaseObjectManager[_UserT], Generic[_UserT]):
    """Query manager for Bitrix24 users."""

    _ORDER_KEY = None

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, _UserT]"]:
        """Return the load API method resolved from the supplied client."""
        return client.user.get

    def filter(self, **filters: Any) -> Self:
        """Return users filtered by SDK object attribute names."""
        return self._filter(**filters)

    def from_pks(self, bitrix_pks: Iterable[int]) -> Self:
        """Return users filtered by Bitrix24 primary keys."""
        return self._from_pks(bitrix_pks)

    def order(self, *fields: Text) -> Self:
        """Return users ordered by SDK object attribute names."""
        return self._order(*fields)

    def select(self, *fields: Text) -> Self:
        """Return users with the requested SDK object fields selected."""
        return self._select(*fields)

    def select_all(self) -> Self:
        """Return users with all registered fields requested."""
        return self._select_all()

    def _add_order_param(self, params: JSONDict):
        """Add ``user.get`` ordering parameters to request parameters."""

        if self._is_fast:
            return

        order_param = self._get_order_param()

        if order_param is None:
            return

        if len(order_param) != 1:
            raise ValueError("user.get supports ordering only by one field.")

        sort, order = next(iter(order_param.items()))

        params["sort"] = sort
        params["order"] = order

    def start(self, start: Optional[int]) -> Self:
        """Return users with a custom Bitrix24 pagination start offset."""
        return self._start(start)

    def add(
            self,
            *,
            email: Text,
            extranet: bool = False,
            sonet_group_ids: Iterable[int] = MISSING,
            timeout: Timeout = None,
            **fields: Any,
    ) -> _UserT:
        """Create an intranet or extranet Bitrix24 user.

        Args:
            email: Required user email address.
            extranet: Whether to create an extranet user. A non-empty
                ``sonet_group_ids`` is required when this is ``True``.
            sonet_group_ids: Workgroup or project IDs for an extranet user.
            timeout: Optional request timeout.
            **fields: User field values keyed by SDK attribute names.

        Raises:
            ValueError: If ``sonet_group_ids`` is omitted or empty for an
                extranet user.
        """

        add_params = None

        if extranet:
            if sonet_group_ids is MISSING:
                raise ValueError("sonet_group_ids is required for an extranet user.")

            if sonet_group_ids.__class__ is not list:
                sonet_group_ids = list(sonet_group_ids)

            add_params = {
                "EXTRANET": "Y",
                "SONET_GROUP_ID": sonet_group_ids,
            }

        return self._add(
            add_params,
            email=email,
            timeout=timeout,
            **fields,
        )

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, _UserT]"]:
        """Return the add API method resolved from the supplied client."""
        return client.user.add

    def add_many(
            self,
            objects_data: Union[Sequence[JSONDict], Mapping[Hashable, JSONDict]],
            *,
            timeout: Timeout = None,
    ) -> BitrixObjectBatchAddResult[_UserT]:
        """Create many Bitrix24 users from SDK field dictionaries."""
        return self._add_many(objects_data, timeout=timeout)

    def update(
            self,
            *,
            timeout: Timeout = None,
            **fields: Any,
    ) -> BitrixObjectBatchWriteResult[_UserT]:
        """Update users matching the current query in batches."""
        return self._update(**fields, timeout=timeout)

    def with_admin_mode(self, admin_mode: bool = True) -> Self:
        """Return users query with the ``ADMIN_MODE`` request parameter."""
        return self._with_params(admin_mode=admin_mode)

    def current(self, *, timeout: Timeout = None) -> _UserT:
        """Return the current Bitrix24 user."""
        return self._client.user.current(timeout=timeout).response.value

    def search(
            self,
            *,
            name: Optional[Text] = MISSING,
            last_name: Optional[Text] = MISSING,
            work_position: Optional[Text] = MISSING,
            uf_department_name: Text = MISSING,
            user_type: Union[Annotated[Text, Literal["email", "employee", "extranet"]], UserType] = MISSING,
            find: Text = MISSING,
    ) -> Self:
        """Return users query that loads results through ``user.search``."""

        filter_params: Optional[JSONDict] = None

        if uf_department_name is not MISSING:
            filter_params = {
                "UF_DEPARTMENT_NAME": uf_department_name,
            }

        filters: JSONDict = {}

        if name is not MISSING:
            filters["name"] = name

        if last_name is not MISSING:
            filters["last_name"] = last_name

        if work_position is not MISSING:
            filters["work_position"] = work_position

        if user_type is not MISSING:
            filters["user_type"] = user_type

        if find is not MISSING:
            if filters or filter_params is not None:
                raise ValueError("user.search does not support mixing 'FIND' with other search fields.")

            filter_params = {
                "FIND": find,
            }

        return self._filter(filter_params, **filters)._with_api_wrapper(
            lambda client: client.user.search,
        )


User.fields = UserFieldManager()
User.objects = UserManager()
