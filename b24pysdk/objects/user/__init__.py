from typing import TYPE_CHECKING, Any, Callable, ClassVar, Iterable, Optional, Text

from ..._constants import MISSING
from ...constants.user import PersonalGender, UserType
from ...schemas.api import BitrixObjectBatchWriteResponse
from ...utils.types import JSONDict, JSONList, Self, Timeout
from .._base_object import BaseObject
from .._managers import BaseFieldManager, BaseObjectManager
from ..fields import BoolField, DateField, DateTimeField, EnumField, IntField, ObjectField, TextField, TimeZoneField, URLField

if TYPE_CHECKING:
    from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
    from ...client import ClientType
    from .._bitrix_object_list import BitrixObjectList
    from ..department import Department

__all__ = [
    "User",
    "UserFieldManager",
    "UserManager",
    "UserUserfield",
    "UserUserfieldManager",
]


class User(BaseObject[int]):
    """Bitrix24 portal user."""

    _PK_TYPE = int
    _UPDATE_KEY = None
    _USERFIELD_AVAILABLE = True

    fields: ClassVar["UserFieldManager"]
    objects: ClassVar["UserManager"]

    bitrix_id = IntField("ID", is_pk=True)
    xml_id = IntField("XML_ID", is_missing_allowed=True)
    active = BoolField("ACTIVE", is_required=True)
    name = TextField("NAME", is_missing_allowed=True)
    last_name = TextField("LAST_NAME", is_missing_allowed=True)
    second_name = TextField("SECOND_NAME", is_missing_allowed=True)
    title = TextField("TITLE", is_missing_allowed=True)
    email = TextField("EMAIL", is_missing_allowed=True)
    last_login = DateTimeField("LAST_LOGIN")
    date_register = DateTimeField("DATE_REGISTER", is_required=True)
    time_zone = TimeZoneField("TIME_ZONE", is_missing_allowed=True)
    is_online = BoolField("IS_ONLINE", is_required=True)
    timestamp_x = DateTimeField("TIMESTAMP_X", is_missing_allowed=True)
    last_activity_date = DateTimeField("LAST_ACTIVITY_DATE", is_missing_allowed=True)
    personal_gender = EnumField("PERSONAL_GENDER", enum_class=PersonalGender)
    personal_www = TextField("PERSONAL_WWW", is_missing_allowed=True)
    personal_birthday = DateField("PERSONAL_BIRTHDAY")
    personal_photo = URLField("PERSONAL_PHOTO", is_missing_allowed=True)
    personal_icq = TextField("PERSONAL_ICQ", is_missing_allowed=True)
    personal_phone = TextField("PERSONAL_PHONE", is_missing_allowed=True)
    personal_fax = TextField("PERSONAL_FAX", is_missing_allowed=True)
    personal_profession = TextField("PERSONAL_PROFESSION", is_missing_allowed=True)
    personal_mobile = TextField("PERSONAL_MOBILE", is_missing_allowed=True)
    personal_pager = TextField("PERSONAL_PAGER", is_missing_allowed=True)
    personal_street = TextField("PERSONAL_STREET", is_missing_allowed=True)
    personal_city = TextField("PERSONAL_CITY", is_missing_allowed=True)
    personal_state = TextField("PERSONAL_STATE", is_missing_allowed=True)
    personal_zip = TextField("PERSONAL_ZIP", is_missing_allowed=True)
    personal_country = TextField("PERSONAL_COUNTRY", is_missing_allowed=True)
    personal_mailbox = TextField("PERSONAL_MAILBOX", is_missing_allowed=True)
    personal_notes = TextField("PERSONAL_NOTES", is_missing_allowed=True)
    work_phone = TextField("WORK_PHONE", is_missing_allowed=True)
    work_company = TextField("WORK_COMPANY", is_missing_allowed=True)
    work_position = TextField("WORK_POSITION", is_missing_allowed=True)
    work_department = TextField("WORK_DEPARTMENT", is_missing_allowed=True)
    work_www = TextField("WORK_WWW", is_missing_allowed=True)
    work_fax = TextField("WORK_FAX", is_missing_allowed=True)
    work_pager = TextField("WORK_PAGER", is_missing_allowed=True)
    work_street = TextField("WORK_STREET", is_missing_allowed=True)
    work_mailbox = TextField("WORK_MAILBOX", is_missing_allowed=True)
    work_city = TextField("WORK_CITY", is_missing_allowed=True)
    work_state = TextField("WORK_STATE", is_missing_allowed=True)
    work_zip = TextField("WORK_ZIP", is_missing_allowed=True)
    work_country = TextField("WORK_COUNTRY", is_missing_allowed=True)
    work_profile = TextField("WORK_PROFILE", is_missing_allowed=True)
    work_logo = TextField("WORK_LOGO", is_missing_allowed=True)
    work_notes = TextField("WORK_NOTES", is_missing_allowed=True)
    uf_skype_link = TextField("UF_SKYPE_LINK", is_missing_allowed=True)
    uf_zoom = TextField("UF_ZOOM", is_missing_allowed=True)
    uf_employment_date = DateField("UF_EMPLOYMENT_DATE")
    uf_timeman = TextField("UF_TIMEMAN", is_missing_allowed=True)
    uf_department_ids = IntField("UF_DEPARTMENT", is_multiple=True, is_missing_allowed=True)
    uf_departments: Optional["BitrixObjectList[Department]"] = ObjectField(uf_department_ids, object_class="..department.Department")
    uf_interests = TextField("UF_INTERESTS", is_missing_allowed=True)
    uf_skills = TextField("UF_SKILLS", is_missing_allowed=True)
    uf_web_sites = TextField("UF_WEB_SITES", is_missing_allowed=True)
    uf_xing = TextField("UF_XING", is_missing_allowed=True)
    uf_linkedin = TextField("UF_LINKEDIN", is_missing_allowed=True)
    uf_twitter = TextField("UF_TWITTER", is_missing_allowed=True)
    uf_skype = TextField("UF_SKYPE", is_missing_allowed=True)
    uf_district = TextField("UF_DISTRICT", is_missing_allowed=True)
    uf_phone_inner = TextField("UF_PHONE_INNER", is_missing_allowed=True)
    user_type = EnumField("USER_TYPE", enum_class=UserType, is_required=True)

    @property
    def url(self) -> Text:
        """Return the absolute Bitrix24 user profile URL."""
        return f"{self._base_url}/company/personal/user/{self.bitrix_pk}/"

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
        """Save local user field changes to Bitrix24."""
        return self._save(update_fields=update_fields, timeout=timeout)


class UserFieldManager(BaseFieldManager[User]):
    """Field metadata manager for Bitrix24 users."""

    __slots__ = ()

    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> JSONDict:
        """Return all Bitrix24 user field metadata."""
        return self._client.user.fields(timeout=timeout).result


class UserManager(BaseObjectManager[User]):
    """Query manager for Bitrix24 users."""

    _ORDER_KEY = None

    __slots__ = ()

    def _get_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValuesRequest[JSONList, User]"]:
        """Return the load API method resolved from the supplied client."""
        return client.user.get

    def filter(self, **filters: Any) -> Self:
        """Return users filtered by SDK object attribute names."""
        return self._filter(**filters)

    def order(self, *fields: Text) -> Self:
        """Return users ordered by SDK object attribute names."""
        return self._order(*fields)

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
            timeout: Timeout = None,
            **fields: Any,
    ) -> User:
        """Create a Bitrix24 user."""
        return self._add(**fields, timeout=timeout)

    def _get_add_api_wrapper(self, client: "ClientType") -> Callable[..., "BitrixAPIValueRequest[int, User]"]:
        """Return the add API method resolved from the supplied client."""
        return client.user.add

    def add_many(
            self,
            items: Iterable[JSONDict],
            *,
            ignore_errors: bool = False,
            timeout: Timeout = None,
    ) -> "BitrixObjectList[User]":
        """Create many Bitrix24 users from SDK field dictionaries."""
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
        """Update users matching the current query in batches."""
        return self._update(**fields, timeout=timeout)

    def admin_mode(self, admin_mode: bool = True) -> Self:
        """Return users query with the ``ADMIN_MODE`` request parameter."""
        return self._with_params(admin_mode=admin_mode)

    def current(self, *, timeout: Timeout = None) -> User:
        """Return the current Bitrix24 user."""
        return self._client.user.current(timeout=timeout).response.value

    def search(
            self,
            *,
            name: Optional[Text] = MISSING,
            last_name: Optional[Text] = MISSING,
            work_position: Optional[Text] = MISSING,
            uf_department_name: Optional[Text] = MISSING,
            user_type: Optional[UserType] = MISSING,
            find: Optional[Text] = MISSING,
    ) -> Self:
        """Return users query that loads results through ``user.search``."""

        filter_param: Optional[JSONDict] = None

        if uf_department_name is not MISSING:
            filter_param = {
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
            if filters or filter_param is not None:
                raise ValueError("user.search does not support mixing 'FIND' with other search fields.")

            filter_param = {
                "FIND": find,
            }

        return self._filter(filter_param, **filters)._with_api_wrapper(
            lambda client: client.user.search,
        )


User.fields = UserFieldManager()
User.objects = UserManager()


from .user_userfield import UserUserfield, UserUserfieldManager  # noqa: E402
