from functools import cached_property
from typing import Annotated, Iterable, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest, BitrixAPIValueRequest, BitrixAPIValuesRequest
from ...constants.group import GroupPermissionRoleLiteral
from ...objects.sonet_group import SonetGroup as SonetGroupObject
from ...utils.converters import bool_to_bitrix
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, JSONList, Timeout
from .._adapters import BitrixObjectAdapter, BitrixObjectsAdapter
from .._base_scope import BaseScope
from .feature import Feature
from .user import User

__all__ = [
    "SonetGroup",
]


class SonetGroup(BaseScope):
    """Class for working with sonet groups.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "sonet_group"

    @cached_property
    def feature(self) -> Feature:
        """"""
        return Feature(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def create(  # noqa: C901, PLR0912
            self,
            name: Text,
            *,
            description: Text = MISSING,
            visible: bool = MISSING,
            opened: bool = MISSING,
            closed: bool = MISSING,
            keywords: Text = MISSING,
            initiate_perms: Annotated[Text, GroupPermissionRoleLiteral] = MISSING,
            project: bool = MISSING,
            project_date_start: Text = MISSING,
            project_date_finish: Text = MISSING,
            scrum_master_id: int = MISSING,
            owner_id: int = MISSING,
            image: Iterable[Text] = MISSING,
            image_file_id: int = MISSING,
            site_id: Iterable[Text] = MISSING,
            subject_id: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValueRequest[int, SonetGroupObject]:
        """Create a group or project

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/sonet-group-create.html

        The method creates a workgroup or project.

        Args:
            name: The name of the group or project;

            description: The description of the group or project;

            visible: The visibility of the group in the list;

            opened: Is the group open for free joining;

            closed: Is the group archived;

            keywords: Keywords separated by commas;

            initiate_perms: Who can invite participants;

            project: Create a project instead of a group;

            project_date_start: The project start date in ISO-8601 format;

            project_date_finish: The project end date in ISO-8601 format;

            scrum_master_id: The identifier of the scrum master if the project is created as scrum;

            owner_id: The identifier of the owner;

            image: The group's avatar in Base64 format;

            image_file_id: The file ID from Drive for setting the avatar;

            site_id: A list of site IDs to which the group is linked;

            subject_id: The identifier of the group's subject;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "NAME": name,
        }

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if visible is not MISSING:
            params["VISIBLE"] = bool_to_bitrix(visible, is_required=True)

        if opened is not MISSING:
            params["OPENED"] = bool_to_bitrix(opened, is_required=True)

        if closed is not MISSING:
            params["CLOSED"] = bool_to_bitrix(closed, is_required=True)

        if keywords is not MISSING:
            params["KEYWORDS"] = keywords

        if initiate_perms is not MISSING:
            params["INITIATE_PERMS"] = initiate_perms

        if project is not MISSING:
            params["PROJECT"] = bool_to_bitrix(project, is_required=True)

        if project_date_start is not MISSING:
            params["PROJECT_DATE_START"] = project_date_start

        if project_date_finish is not MISSING:
            params["PROJECT_DATE_FINISH"] = project_date_finish

        if scrum_master_id is not MISSING:
            params["SCRUM_MASTER_ID"] = scrum_master_id

        if owner_id is not MISSING:
            params["OWNER_ID"] = owner_id

        if image is not MISSING:
            if image.__class__ is not list:
                image = list(image)

            params["IMAGE"] = image

        if image_file_id is not MISSING:
            params["IMAGE_FILE_ID"] = image_file_id

        if site_id is not MISSING:
            if site_id.__class__ is not list:
                site_id = list(site_id)

            params["SITE_ID"] = site_id

        if subject_id is not MISSING:
            params["SUBJECT_ID"] = subject_id

        return self._make_bitrix_api_request(
            api_wrapper=self.create,
            params=params,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValueRequest,
            result_adapter=BitrixObjectAdapter("sonet_group", client=self._client),
        )

    @type_checker
    def delete(
            self,
            group_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete group or project

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/sonet-group-delete.html

        The method removes a workgroup or project.

        Args:
            group_id: Identifier of the group or project to be deleted;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "GROUP_ID": group_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            group_id: int = MISSING,
            order: JSONDict = MISSING,
            filter: JSONDict = MISSING,
            is_admin: bool = MISSING,
            start: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIValuesRequest[JSONList, SonetGroupObject]:
        """Get a list of groups and projects

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/sonet-group-get.html

        The method returns a list of workgroups and projects considering the permissions of the current user.

        Args:
            group_id: Identifier of the group or project;

            order: An object for sorting the selected records, where the key is the field and the value is ASC or DESC;

            filter: Object for filtering;

            is_admin: Disable permission check;

            start: Pagination parameter;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if group_id is not MISSING:
            params["GROUP_ID"] = group_id

        if order is not MISSING:
            params["ORDER"] = order

        if filter is not MISSING:
            params["FILTER"] = filter

        if is_admin is not MISSING:
            params["IS_ADMIN"] = bool_to_bitrix(is_admin, is_required=True)

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
            bitrix_api_request_type=BitrixAPIValuesRequest,
            result_adapter=BitrixObjectsAdapter("sonet_group", client=self._client),
        )

    @type_checker
    def setowner(
            self,
            group_id: int,
            user_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Change the owner of a group or project

        Documentation:https://apidocs.bitrix24.com/api-reference/sonet-group/sonet-group-setowner.html

        The method assigns a new owner to a workgroup or project.

        Args:
            group_id: Identifier of the group or project;

            user_id: Identifier of the new owner;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.setowner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(  # noqa: C901, PLR0912
            self,
            group_id: int,
            *,
            name: Text = MISSING,
            description: Text = MISSING,
            visible: bool = MISSING,
            opened: bool = MISSING,
            closed: bool = MISSING,
            keywords: Text = MISSING,
            initiate_perms: Annotated[Text, GroupPermissionRoleLiteral] = MISSING,
            project_date_start: Text = MISSING,
            project_date_finish: Text = MISSING,
            owner_id: int = MISSING,
            image: Iterable[Text] = MISSING,
            image_file_id: int = MISSING,
            site_id: Iterable[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[int]:
        """Change group or project

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/sonet-group-update.html

        The method modifies the parameters of a workgroup or project.

        Args:
            group_id: Identifier of the group or project;

            name: New name;

            description: The description of the group or project;

            visible: The visibility of the group in the list;

            opened: Is the group open for free joining;

            closed: Is the group archived;

            keywords: Keywords separated by commas;

            initiate_perms: Who can invite participants;

            project_date_start: The project start date in ISO-8601 format;

            project_date_finish: The project end date in ISO-8601 format;

            owner_id: The identifier of the owner;

            image: The group's avatar in Base64 format;

            image_file_id: The file ID from Drive for setting the avatar;

            site_id: A list of site IDs to which the group is linked;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "GROUP_ID": group_id,
        }

        if name is not MISSING:
            params["NAME"] = name

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if visible is not MISSING:
            params["VISIBLE"] = bool_to_bitrix(visible, is_required=True)

        if opened is not MISSING:
            params["OPENED"] = bool_to_bitrix(opened, is_required=True)

        if closed is not MISSING:
            params["CLOSED"] = bool_to_bitrix(closed, is_required=True)

        if keywords is not MISSING:
            params["KEYWORDS"] = keywords

        if initiate_perms is not MISSING:
            params["INITIATE_PERMS"] = initiate_perms

        if project_date_start is not MISSING:
            params["PROJECT_DATE_START"] = project_date_start

        if project_date_finish is not MISSING:
            params["PROJECT_DATE_FINISH"] = project_date_finish

        if owner_id is not MISSING:
            params["OWNER_ID"] = owner_id

        if image is not MISSING:
            if image.__class__ is not list:
                image = list(image)

            params["IMAGE"] = image

        if image_file_id is not MISSING:
            params["IMAGE_FILE_ID"] = image_file_id

        if site_id is not MISSING:
            if site_id.__class__ is not list:
                site_id = list(site_id)

            params["SITE_ID"] = site_id

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
